from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from utils.log_utils import log_action
import constants
import os
from dotenv import load_dotenv

load_dotenv()


# Establish a connection to the Clarifai API
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)


metadata = (('authorization', 'Key ' + os.getenv('CLARIFAI_TOKEN')),)

userDataObject = resources_pb2.UserAppIDSet(user_id='clarifai', app_id='main')

# Send image to Clarifai API
def send_image_to_clarifai(image):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id='general-image-recognition',
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        log_action(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0]
    return output

def get_label_matches(output):
    matched_labels = []
    for concept in output.data.concepts:
        if (concept.name.lower() in [label.lower() for label in constants.FOOD_LABELS]):
            if (float(concept.value) >= constants.FOOD_LABEL_THRESHOLD):
                matched_labels.append(concept.name)

    if len(matched_labels) > 2:
        log_action("Matched labels:", matched_labels)
        return True
    else:
        log_action("No matching labels found")
        return False
