import os
import glob
import pathlib
from datetime import datetime
from irods.meta import iRODSMeta, AVUOperation
from irods.models import Collection
from gitirods.iinit.session import renewIrodsSession
from gitirods.iinit.session import SimpleiRODSSession
from gitirods.util import getRepo, configReader, addAtomicMetadata


def readExternalRepo(path):
    """
    Reader function:
    Reads the content of '.repos' file in the repository
    and retuns.
    Parameters
    ----------
    path : directoy/file
    Returns
    -------
    externalRepoPaths : list
    """

    filename = path + '/.repos'
    externalRepoPaths = []
    try:
        with open(filename, 'r+') as f:
            for line in f:
                externalRepoPaths.append(line.strip('\n'))
        return externalRepoPaths
    except OSError as error:
        print(f'{type(error)}: {error}')


def defineMetadataForCheckPoint():
    """
    Metadata constructor function:
    Specifies metadata that will be added on check point collection
    based on the last commit, repository url and user input.
    Returns
    -------
    checkPointComment, commitID, commitMessage, projectRepoURL : str
    """

    checkPointCommentInput = input('Write Checkpoint comment: ')
    checkPointComment = checkPointCommentInput.rstrip()
    repo, _ = getRepo()
    master = repo.head.reference
    commitID = master.commit.hexsha
    commitMessage = master.commit.message
    commitMessage = commitMessage.rstrip()
    committerName = master.commit.author.name
    committerMail = master.commit.author.email
    projectRepoURL = repo.remotes.origin.url
    return checkPointComment, projectRepoURL, commitID, \
            commitMessage, committerName, committerMail


def defineExternalReposMetadata(path):
    """
    Metadata add function:
    Annotate AVUs extracted from the repositories written in '.repos' file
    to the checkpoint collections.
    Parameters
    ----------
    avus (str): external repository directoy
    Returns
    -------
    avus (dict): metadata attrs values extracted from external repositories
    """

    externalRepoPaths = readExternalRepo(path)
    avus = {}
    for item in externalRepoPaths:
        repo, repository_path = getRepo(item)
        master = repo.head.reference
        commitID_external = master.commit.hexsha
        commitMessage_external = master.commit.message
        commitMessage_external = commitMessage_external.rstrip()
        projectRepoURL_external = repo.remotes.origin.url
        repoBaseName = os.path.basename(repository_path)
        avus[f'user.git.hooks.external_repository_url_{repoBaseName}'] = projectRepoURL_external
        avus[f'user.git.hooks.external_commit_id_{repoBaseName}'] = commitID_external
        avus[f'user.git.hooks.external_commit_message_{repoBaseName}'] = commitMessage_external
    return avus


def makeArchive():
    """
    Archive function:
    Creates an archive file from the current HEAD ref of the repository
    in zip format.
    """

    repo, _ = getRepo()
    repo.git.archive('--format=zip', '-o', 'archive.zip', 'HEAD')


def uploadArchive(session, repositoryPath, checkPointPath):
    """
    Upload function:
    It uploads an archive file to iRODS - inside checkpoint collection,
    and if needed it creates sub-collections in iRODS.
    Parameters
    ----------
    session : an iRODS session object
    repositoryPath : repository path in the local file system
    checkPointPath : checkpoint collection path in iRODS
    """

    makeArchive()
    source_path = os.path.join(repositoryPath, 'archive.zip')
    destination_path = os.path.join(checkPointPath, 'archive.zip')
    session.data_objects.put(source_path, destination_path)
    os.remove(source_path)


def walkRecursive(path):
    """
    A generator function:
    Yields local root directory path and/or local files path.
    It walks from a root parent to sub dirs and
    returns a generator object.
    Parameters
    ----------
    path : out* directory path
    Returns
    -------
    A generator object for local dirs and file paths
    """

    for root, _, files in os.walk(path):
        local_dir = root.split(os.sep)[5:]
        local_dir_path = '/'.join(local_dir)
        yield local_dir_path
        for name in files:
            local_files_path = os.path.join(root, name)
            yield local_files_path


def iputCollection(session, sourcePath, destPath):
    """
    A recursive collection upload function:
    Upload the out* directories' local files and/or folders to the iRODS,
    in a manner that resembles the iCommands 'iput -r' command.
    Parameters
    ----------
    session : an iRODS session object
    sourcePath : git repository path on the local file system
    destPath : iRODS path >
                /zone/home/groupCol/repositories/repoName/checkPointName
    """

    out_dirs = glob.glob(sourcePath + '/out*')
    for item in out_dirs:
        for path in walkRecursive(item):
            if os.path.isdir(path):
                target_coll = os.path.join(destPath, path)
                session.collections.create(target_coll)
            elif os.path.isfile(path):
                file_name = os.path.basename(path)
                session.data_objects.put(path, target_coll + '/' + file_name)


def createCheckPoint(group_name=None):
    """
    Create check point function:
    It names the checkpoint based on user inout and date time
    and creates the checkpoint collection. Finally it adds specified
    metadata on the check point collection and calls upload function.
    Parameter
    ----------
    group_name : group name in an iRODS zone (default is None)
    """

    if group_name is None:
        config = configReader()
        data = config.items('DEFAULT')
        group_name = data[1][1]
    _, repositoryPath = getRepo()
    repositoryName = pathlib.PurePath(repositoryPath).name
    # Name the new checkpoint and metadata
    checkPointInput = input('Write your Checkpoint name: ')
    checkPointInput = checkPointInput.upper()
    checkPointNameExtension = datetime.today().strftime('%Y%m%d_%H%M')
    # Define metadata
    attributes = ['user.git.hooks.check_point_comment', 'user.git.hooks.project_repository_url', \
                  'user.git.hooks.project_repository_commit_ID', 'user.git.hooks.project_repository_commit_message', \
                  'user.git.hooks.project_repository_committer_name', 'user.git.hooks.project_repository_commit_mail']
    values = defineMetadataForCheckPoint()
    values = list(values)
    # Use a single seesion to create a check point collection, to upload data and to add metadata. 
    with SimpleiRODSSession() as session:
        # Query to get iRODS path for the repository collection
        zone_name = session.zone
        query = session.query(Collection)
        query_filter = query.filter(Collection.name == f'/{zone_name}/home/{group_name}/repositories')
        irods_path_list = [item[Collection.name] for item in query_filter]
        irodsPath = irods_path_list[0] + '/' + repositoryName
        checkPointName = f'{checkPointInput}-{checkPointNameExtension}'
        checkPointPath = irodsPath + '/' + checkPointName
        # Create check point collection
        session.collections.create(checkPointPath)
        coll = session.collections.get(checkPointPath)
        iputCollection(session, repositoryPath, checkPointPath)
        uploadArchive(session, repositoryPath, checkPointPath)
        external_repos = repositoryPath + '/.repos'
        addAtomicMetadata(coll, attributes, values,
            external_repos=external_repos, func=defineExternalReposMetadata)



def executeCheckPoint():
    """
    Executer function:
    Once the checkpoint input is received, it executes required fucntions.
    """

    checkPointQuestion = input('Is a checkpoint reached? [yes/Y or no/N] ')
    checkPointQuestion = checkPointQuestion.upper()
    checkPointQuestion = checkPointQuestion.replace('YES', 'Y')
    checkPointQuestion = checkPointQuestion.replace('NO', 'N')
    try:
        if checkPointQuestion == 'Y':
            renewIrodsSession()
            createCheckPoint()
            print('Completed!')
            return True
        elif checkPointQuestion == 'N':
            print('You are making a normal commit.')
            return False
        else:
            print('Invalid Input')
            return executeCheckPoint()
    except Exception as error:
        print('Please enter valid inputs')
        print(error)
        return executeCheckPoint()
