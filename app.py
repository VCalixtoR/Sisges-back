from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from utils.dbUtils import dbCheckCreate
from utils.cryptoFunctions import loadGenerateKeys
from utils.eventScheduler import addToEventScheduler, printEventSchedulerInfo, startEventScheduler
from utils.sistemConfig import sisConfigStart, getMissingEnvironmentVar
from utils.smtpMails import startSmtpServer, addToSmtpMailServer

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

  tmpSeconds = 0
  addToEventScheduler(1, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = -10
  addToEventScheduler(2, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 20
  addToEventScheduler(3, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 5
  addToEventScheduler(4, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 2
  addToEventScheduler(5, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 7
  addToEventScheduler(6, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 15
  addToEventScheduler(7, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 15
  addToEventScheduler(8, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 19
  addToEventScheduler(9, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  tmpSeconds = 1
  addToEventScheduler(10, tmpSeconds, addToSmtpMailServer, {
    'rawTo': 'test@ufu.br',
    'rawSubject': f'test with {tmpSeconds} seconds',
    'rawBody': f'this has sended by event scheduler with {tmpSeconds} timestamp seconds'})
  printEventSchedulerInfo()

test()