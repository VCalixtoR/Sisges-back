from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from utils.dbUtils import dbCheckCreate
from utils.cryptoFunctions import loadGenerateKeys
from utils.eventScheduler import addMailToEventScheduler, printEventSchedulerInfo, startEventScheduler
from utils.sistemConfig import sisConfigStart, getMissingEnvironmentVar
from utils.smtpMails import startSmtpServer

from services.authentication import Login, Sign
from services.advisors import Advisors
from services.dynamicPage import DynamicPage
from services.fileTransmission import FileTransmission
from services.sendMail import SendMail
from services.solicitations import CoordinatorSolicitations, AdvisorSolicitations, StudentSolicitations
from services.solicitation import Solicitation
from services.solicitationAdvisor import SolicitationAdvisor
from services.solicitationTransitions import SolicitationTransitions
from services.reasons import Reasons

# create flask api server with enabled Authorization cors to all origins used to do user authentication
app = Flask(__name__)
CORS(
  app,
  origins='*',
  headers=["Content-Type", "Authorization"],
  expose_headers="Authorization")

# set service endpoints
api = Api(app)
api.add_resource(Login, "/login")
api.add_resource(Sign, "/sign")
api.add_resource(FileTransmission, "/file")
api.add_resource(DynamicPage, "/dynamicpage")
api.add_resource(CoordinatorSolicitations, "/coordinator/solicitations")
api.add_resource(Advisors, "/advisors")
api.add_resource(AdvisorSolicitations, "/advisor/solicitations")
api.add_resource(SendMail, "/sendmail")
api.add_resource(StudentSolicitations, "/student/solicitations")
api.add_resource(Solicitation, "/solicitation")
api.add_resource(SolicitationAdvisor, "/solicitation/advisor")
api.add_resource(SolicitationTransitions, "/solicitation/transitions")
api.add_resource(Reasons, "/reasons")

# For homol and production ambients like render.com the environment variables are already loaded
if getMissingEnvironmentVar():
  print("# Loading and checking environment from .env")

  load_dotenv(find_dotenv())
  missingVar = getMissingEnvironmentVar()
  if missingVar:
    print("# Error - Missing " + str(missingVar) + " environment variable")
    exit()
  
# Start MySQL
dbCheckCreate()
# Start SMTP Server
startSmtpServer()
# Load System Configutations
sisConfigStart()
# Load Secret Keys
loadGenerateKeys()
# Load System Event Scheduler
startEventScheduler

# For testing
def test():
  seconds = [0, -10, 20, 5, 2, 7, 15, 15, 19, 1]
  for second in seconds:
    addMailToEventScheduler(1, datetime.now()+timedelta(0, second),
      'test@ufu.br', f'test with {second} seconds', f'this has sended by event scheduler with {second} timestamp seconds')
  printEventSchedulerInfo()
test()