from flask import Flask, abort, request
from flask_restful import Resource, Api, reqparse
import traceback

from utils.dbUtils import *
from utils.cryptoFunctions import isAuthTokenValid

def getTransitions(solicitationStateIdFrom):

  tsQuery = None
  try:
    
    sqlQuery = """
      SELECT sst.id, sst.solicitation_state_id_from, sst.solicitation_state_id_to, sst.transition_name, 
        sstm.solicitation_state_transition_id AS manual_transition_id, sstm.transition_decision AS manual_transition_decision, 
        sstm.transition_reason AS manual_transition_reason, 
                       
        sstdp.solicitation_state_transition_id AS dynamic_page_transition_id, 
        sstdp.dynamic_page_component, sstdp.transition_decision AS component_transition_decision, 
        sstdp.transition_reason AS component_transition_reason,

        ssts.solicitation_state_transition_id AS scheduled_transition_id, ssts.transition_decision AS scheduled_transition_decision, 
        ssts.transition_reason AS scheduled_transition_reason, ssts.transition_delay_seconds AS scheduled_transition_delay_seconds 

          FROM solicitation_state_transition sst 
          LEFT JOIN solicitation_state_transition_manual sstm ON sst.id = sstm.solicitation_state_transition_id 
          LEFT JOIN solicitation_state_transition_from_dynamic_page sstdp ON sst.id = sstdp.solicitation_state_transition_id 
          LEFT JOIN solicitation_state_transition_scheduled ssts ON sst.id = ssts.solicitation_state_transition_id 

          WHERE sst.solicitation_state_id_from = %s;
    """
    tsQuery = dbGetAll(sqlQuery,(solicitationStateIdFrom,))

  except Exception as e:
    print("# Database reading error:")
    print(str(e))
    traceback.print_exc()
    return "Erro na base de dados", 409

  if not tsQuery:
    return []
  
  tsParsed = []
  for transition in tsQuery:
    obj = {
      "id": transition["id"],
      "transition_name": transition["transition_name"],
      "solicitation_state_id_from": transition["solicitation_state_id_from"],
      "solicitation_state_id_to": transition["solicitation_state_id_to"]
    }
    if transition["manual_transition_id"]:
      obj["type"] = "manual"
      obj["transition_decision"] = transition["manual_transition_decision"]
      obj["transition_reason"] = transition["manual_transition_reason"]
    
    if transition["dynamic_page_transition_id"]:
      obj["type"] = "from_dynamic_page"
      obj["dynamic_page_component"] = transition["dynamic_page_component"]
      obj["transition_decision"] = transition["component_transition_decision"]
      obj["transition_reason"] = transition["component_transition_reason"]
    
    if transition["scheduled_transition_id"]:
      obj["type"] = "scheduled"
      obj["transition_decision"] = transition["scheduled_transition_decision"]
      obj["transition_reason"] = transition["scheduled_transition_reason"]
      obj["transition_delay_seconds"] = transition["scheduled_transition_delay_seconds"]

    tsParsed.append(obj)
  
  return tsParsed

# Data from solicitation transitions (State machine)
class SolicitationTransitions(Resource):

  # get transitions data
  def get(self):

    args = reqparse.RequestParser()
    args.add_argument("Authorization", location="headers", type=str, help="Bearer with jwt given by server in user autentication, required", required=True)
    args.add_argument("solicitation_state_id_from", location="args", type=int)
    args = args.parse_args()

    # verify jwt and its signature correctness
    isTokenValid, errorMsg, _ = isAuthTokenValid(args)
    if not isTokenValid:
      abort(401, errorMsg)

    print("\n# Starting get solicitation transitions\n# Reading data from DB")
    tsData = getTransitions(args["solicitation_state_id_from"])
    print("# Operation Done!")
    
    return tsData, 200