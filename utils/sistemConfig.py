from utils.dbUtils import *
from pathlib import Path
# pathlib paths works both for windows and unix OSs

keyFilesPath = None
userFilesPath = None

def getMissingEnvironmentVar():

  if not os.getenv('FRONT_BASE_URL'):
    return 'FRONT_BASE_URL'
  
  if not os.getenv('SQL_HOST'):
    return 'SQL_HOST'
  if not os.getenv('SQL_SCHEMA'):
    return 'SQL_SCHEMA'
  if not os.getenv('SQL_PORT'):
    return 'SQL_PORT'
  if not os.getenv('SQL_USER'):
    return 'SQL_USER'
  if not os.getenv('SQL_PASSWORD'):
    return 'SQL_PASSWORD'
  
  if not os.getenv('SMTP_HOST'):
    return 'SMTP_HOST'
  if not os.getenv('SMTP_PORT'):
    return 'SMTP_PORT'
  if not os.getenv('SMTP_LOGIN'):
    return 'SMTP_LOGIN'
  if not os.getenv('SMTP_PASSWORD'):
    return 'SMTP_PASSWORD'

  if not os.getenv('SYS_DEBUG'):
    return 'SYS_DEBUG'

  return None

def sisConfigStart():
  loadPaths()

def loadPaths():

  global keyFilesPath, userFilesPath
  
  if not keyFilesPath or not userFilesPath:

    keyFilesPath = None
    userFilesPath = None

    queryRes = []
    try:
      queryRes = dbGetAll(
        ' SELECT nome, path_str ' \
	      '   FROM config AS c JOIN config_path AS cp ON c.id = cp.config_id; ')
      
      if not queryRes:
        raise Exception('No return for sistem root config path query ' + str(queryRes))

      # Set root path for both OSs
      for cpath in queryRes:
        if cpath[0] == 'root path key files':
          keyFilesPath = Path(cpath[1])
        elif cpath[0] == 'root path user files':
          userFilesPath = Path(cpath[1])
      
      if not keyFilesPath or not userFilesPath:
        raise Exception('Missing config paths')
    
    except Exception as e:
      print('# Database config reading error:')
      print(str(e))
    
    # creates paths if not exists
    keyFilesPath.mkdir(parents=True, exist_ok=True)
    userFilesPath.mkdir(parents=True, exist_ok=True)

    print('# Key files path: ' + str(keyFilesPath.resolve()))
    print('# User file storage root path: ' + str(userFilesPath.resolve()))

def getKeysFilePath(keyFileName):
  global keyFilesPath
  return keyFilesPath / keyFileName

def getUserFilesPath(userFileHash):
  global userFilesPath
  return userFilesPath / userFileHash