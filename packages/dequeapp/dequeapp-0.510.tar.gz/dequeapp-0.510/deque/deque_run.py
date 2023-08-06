import datetime
import json
import os
import subprocess
import traceback

import coolname

from deque.rest_connect import RestConnect
from deque.deque_environment import AGENT_API_SERVICE_URL
from deque.redis_services import RedisServices
import pickle
import multiprocessing
from deque.parsing_service import ParsingService
from deque.datatypes import Image, Audio, Histogram, BoundingBox2D

'''
def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj
'''

def _start_transport_service():
    try:
        print("Starting transport")
        import redis_server
        bin_path = str(redis_server.REDIS_SERVER_PATH)
        subprocess.run([bin_path])
        print("started successfully")
    except Exception as e:
        print(e)
        traceback.print_exc()

_start_transport_service()

class Run:

    #_submission_count = 1
    def __init__(self):
        self.user_name = None

        self._workload_type = None
        #self._submission_id = None

        self.project_id = None
        self._project_name = None

        self.params = dict()
        self._history = dict()
        self._step=1
        self._run_id = None
        self._rest = RestConnect()
        self._redis = RedisServices.get_redis_connection()

    def init(self, user_name=None, project_name=None):
        self.user_name = user_name




        self._workload_type = os.getenv("workload_type")
        self._workload_id = os.getenv("workload_id")
        self._submission_id = os.getenv("submission_id")

        if project_name is None:
            if self._workload_id is None:
                raise ValueError("Project name cannot be empty")
            else:
                self._project_name = self._workload_id
        else:
            self._project_name = project_name
        self._run_id = str(coolname.generate_slug(2))
        self._step = 1


        p2 = multiprocessing.Process(target=self.start_parser)
        p2.start()
        self._redis.flushall()
        self._redis.sadd("run_ids:", self._run_id)
        print("Run initialized with run id: "+ self._run_id)

    '''
    def _generate_submission_id(self):
        req_data = {"submission_id":self._submission_id,"user_name":self.user_name,"workload_type":self._workload_type,"workload_id":self._workload_id}
        resp = self._rest.post(AGENT_API_SERVICE_URL+"/fex/submission/exists/",json=req_data)
        resp_data = resp.json()
        if resp_data["exists"]==True:
            self._submission_id = str(coolname.generate_slug(2))

            self._version_code()
            req_data = {"submission_id": self._submission_id, "user_name": self.user_name,
                        "workload_type": self._workload_type, "workload_id": self._workload_id,"parent_submission_id":self._parent_submission_id}
            resp = self._rest.post(AGENT_API_SERVICE_URL + "/fex/submission/create/", json=req_data)
            Run._submission_count+=1




    def _version_code(self):

        # by updating the submission_id in the environment variable, the agent will not autosave to the new submission
        full_env_var = "notebook_submission_details"
        current_submissions_str = os.getenv(full_env_var)
        if current_submissions_str is not None:

            current_submissions = json.loads(current_submissions_str)

            for submission in current_submissions:
                if self._workload_id == submission['notebook_id']:
                    submission.update({"submission_id":self._submission_id})
                    break

            os.environ[full_env_var] = json.dumps(current_submissions)
        else:
            print("Auto-Versioning failed. Please press Command-S")


    '''

    def start_parser(self):
        parser = ParsingService()
        parser.receive()

    def send_data_to_redis(self, step, data):

        key = "run_id:step:data:" + self._run_id + str(step)

        self._redis.sadd("run_id:steps:" + self._run_id, str(step))

        data_pickled = pickle.dumps(data)

        self._redis.set(key, data_pickled)

    def log(self, data, step=None, commit=True):
        #self._validate_data(data=data)
        full_data = {"experiment_data":data}
        full_data.update(
            {"user_name": self.user_name, "run_id": self._run_id,"workload_type": self._workload_type,
             "workload_id": self._workload_id,"submission_id":self._submission_id,
             "project_name": self._project_name, "deque_log_time": datetime.datetime.now(), "step": self._step})

        self.send_data_to_redis(step=self._step, data=full_data)
        if commit:
            self._step += 1

    def _validate_data(self, data):
        for key, value in data.items():
            if type(value) is dict:
                self._validate_data(value)
            else:
                #print(type(value))
                if type(value) in [Audio, BoundingBox2D, Histogram,
                                   Image] or value.__class__.__module__ == '__builtin__':
                    pass
                else:
                    raise ValueError(
                        "Invalid type in dictionary. Allowed values include builtin types and Deque data types "+ str(type(value)) + " "+ str(value.__class__.__module__ ))

    def send_upstream(self):
        self._rest.post(url=AGENT_API_SERVICE_URL + "/fex/python/track/", json=self._history)
        self._history = dict()


if __name__ == "__main__":
    deque = Run()
    #deque.init(user_name="riju@deque.app", project_name="awesome-dude")
    #for i in range(100):
        #deque.log(data={"train": {"accuracy": i, "loss": i - 100}, "image": deque.im})

    # deque.log(data={"image":deque.im})
