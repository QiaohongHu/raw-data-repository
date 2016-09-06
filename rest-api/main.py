import config
import datetime
import db
import endpoints
import evaluation
import participant
import uuid
from protorpc import message_types
from protorpc import messages
from protorpc import remote


# ResourceContainers are used to encapsulate a request body and URL
# parameters. This one is used to represent the participant ID for the
# participant_get method.
GET_PARTICIPANT_RESOURCE = endpoints.ResourceContainer(
    # The request body should be empty.
    message_types.VoidMessage,
    # Accept one URL parameter: a string named 'id'
    participant_id=messages.StringField(1, variant=messages.Variant.STRING))

UPDATE_PARTICIPANT_RESOURCE = endpoints.ResourceContainer(
    participant.ParticipantResource,
    # Accept one URL parameter: a string named 'id'
    participant_id=messages.StringField(1, variant=messages.Variant.STRING))

GET_EVALUATION_RESOURCE = endpoints.ResourceContainer(
    # The request body should be empty.
    message_types.VoidMessage,
    evaluation_id=messages.StringField(1, variant=messages.Variant.STRING),
    participant_id=messages.StringField(2, variant=messages.Variant.STRING))

LIST_EVALUATION_RESOURCE = endpoints.ResourceContainer(
    # The request body should be empty.
    message_types.VoidMessage,
    participant_id=messages.StringField(2, variant=messages.Variant.STRING))

UPDATE_EVALUATION_RESOURCE = endpoints.ResourceContainer(
    evaluation.EvaluationResource,
    evaluation_id=messages.StringField(1, variant=messages.Variant.STRING),
    participant_id=messages.StringField(2, variant=messages.Variant.STRING))

# Data Access Objects
participant_dao = participant.Participant()
evaluation_dao = evaluation.Evaluation()


@endpoints.api(name='participant',
               version='v1',
               allowed_client_ids=config.ALLOWED_CLIENT_IDS,
               scopes=[endpoints.EMAIL_SCOPE])
class ParticipantApi(remote.Service):

  @endpoints.method(
      # This method does not take a request message.
      message_types.VoidMessage,
      # This method returns a ParticipantCollection message.
      participant.ParticipantCollection,
      path='participants',
      http_method='GET',
      name='participants.list')
  def list_participants(self, unused_request):
    return participant_dao.List({})

  @endpoints.method(
      participant.ParticipantResource,
      participant.ParticipantResource,
      path='participants',
      http_method='POST',
      name='participants.insert')
  def insert_participant(self, request):
    request.participant_id = str(uuid.uuid4())
    return participant_dao.Insert(request)

  @endpoints.method(
      UPDATE_PARTICIPANT_RESOURCE,
      participant.ParticipantResource,
      path='participants/{participant_id}',
      http_method='PUT',
      name='participants.update')
  def update_participant(self, request):
    return participant_dao.Update(request)

  @endpoints.method(
      # Use the ResourceContainer defined above to accept an empty body
      # but an ID in the query string.
      GET_PARTICIPANT_RESOURCE,
      # This method returns a participant.
      participant.ParticipantResource,
      # The path defines the source of the URL parameter 'id'. If not
      # specified here, it would need to be in the query string.
      path='participants/{participant_id}',
      http_method='GET',
      name='participants.get')
  def get_participant(self, request):
    try:
      # request.participant_id is used to access the URL parameter.
      return participant_dao.Get(request)
    except IndexError:
      raise endpoints.NotFoundException('Participant {} not found'.format(
          request.participant_id))

  @endpoints.method(
      GET_EVALUATION_RESOURCE,
      # This method returns a ParticipantCollection message.
      evaluation.EvaluationCollection,
      path='participants/{participant_id}/evaluations',
      http_method='GET',
      name='evaluations.list')
  def list_evaluations(self, request):
    return evaluation_dao.List(request)

  @endpoints.method(
      UPDATE_EVALUATION_RESOURCE,
      evaluation.EvaluationResource,
      path='participants/{participant_id}/evaluations',
      http_method='POST',
      name='evaluations.insert')
  def insert_evaluation(self, request):
    return evaluation_dao.Insert(request)

  @endpoints.method(
      UPDATE_EVALUATION_RESOURCE,
      evaluation.EvaluationResource,
      path='participants/{participant_id}/evaluations/{evaluation_id}',
      http_method='PUT',
      name='evaluations.update')
  def update_evaluation(self, request):
    return evaluation_dao.Update(request)

  @endpoints.method(
      # Use the ResourceContainer defined above to accept an empty body
      # but an ID in the query string.
      GET_EVALUATION_RESOURCE,
      # This method returns a evaluation.
      evaluation.EvaluationResource,
      # The path defines the source of the URL parameter 'id'. If not
      # specified here, it would need to be in the query string.
      path='participants/{participant_id}/evaluations/{evaluation_id}',
      http_method='GET',
      name='evaluations.get')
  def get_evaluation(self, request):
    try:
      return evaluation_dao.Get(request.participant_id, request.evaluation_id)
    except IndexError:
      raise endpoints.NotFoundException(
          'Evaluation participant_id: {} evaluation_id: not found'.format(
              request.participant_id, request.evaluation_id))

api = endpoints.api_server([ParticipantApi])
