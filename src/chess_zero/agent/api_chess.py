# """
# Defines the process which will listen on the pipe for
# an observation of the game state and return a prediction from the policy and
# value network.
# """
# from multiprocessing import connection, Pipe
# from threading import Thread

# import numpy as np

# from chess_zero.config import Config


# class ChessModelAPI:
#     """
#     Defines the process which will listen on the pipe for
#     an observation of the game state and return the predictions from the policy and
#     value networks.
#     Attributes:
#         :ivar ChessModel agent_model: ChessModel to use to make predictions.
#         :ivar list(Connection): list of pipe connections to listen for states on and return predictions on.
#     """
#     # noinspection PyUnusedLocal
#     def __init__(self, agent_model):  # ChessModel
#         """

#         :param ChessModel agent_model: trained model to use to make predictions
#         """
#         self.agent_model = agent_model
#         self.pipes = []


#     def start(self):
#         """
#         Starts a thread to listen on the pipe and make predictions
#         :return:
#         """
#         prediction_worker = Thread(target=self._predict_batch_worker, name="prediction_worker")
#         prediction_worker.daemon = True
#         prediction_worker.start()

#     def create_pipe(self):
#         """
#         Creates a new two-way pipe and returns the connection to one end of it (the other will be used
#         by this class)
#         :return Connection: the other end of this pipe.
#         """
#         me, you = Pipe()
#         self.pipes.append(me)
#         return you

#     def _predict_batch_worker(self):
#         """
#         Thread worker which listens on each pipe in self.pipes for an observation, and then outputs
#         the predictions for the policy and value networks when the observations come in. Repeats.
#         """
#         while True:
#             ready = connection.wait(self.pipes,timeout=0.001)
#             if not ready:
#                 continue
#             data, result_pipes = [], []
#             for pipe in ready:
#                 while pipe.poll():
#                     data.append(pipe.recv())
#                     result_pipes.append(pipe)

#             data = np.asarray(data, dtype=np.float32)
#             policy_ary, value_ary = self.agent_model.model.predict_on_batch(data)
#             for pipe, p, v in zip(result_pipes, policy_ary, value_ary):
#                 pipe.send((p, float(v)))

"""
Defines the process which will listen on the pipe for
an observation of the game state and return a prediction from the policy and
value network.
"""

from multiprocessing import connection, Pipe
from threading import Thread
import numpy as np


class ChessModelAPI:
    """
    Defines the process which will listen on the pipe for
    an observation of the game state and return the predictions from the policy and
    value networks.
    """

    def __init__(self, agent_model):
        self.agent_model = agent_model
        self.pipes = []

    def start(self):
        prediction_worker = Thread(target=self._predict_batch_worker, name="prediction_worker")
        prediction_worker.daemon = True
        prediction_worker.start()

    def create_pipe(self):
        me, you = Pipe()
        self.pipes.append(me)
        return you

    def _predict_batch_worker(self):
        while True:
            ready = connection.wait(self.pipes, timeout=0.001)
            if not ready:
                continue

            data, result_pipes = [], []
            for pipe in ready:
                while pipe.poll():
                    data.append(pipe.recv())
                    result_pipes.append(pipe)

            import tensorflow as tf
            import numpy as np

            data = np.asarray(data, dtype=np.float32)
            policy_ary, value_ary = self.agent_model.model.predict_on_batch(data)

            for pipe, p, v in zip(result_pipes, policy_ary, value_ary):
                pipe.send((p, float(v)))


# === TEST MODE ===
if __name__ == "__main__":
    from chess_zero.agent.model_chess import ChessModel
    from chess_zero.config import Config
    import os

    config = Config()
    model = ChessModel(config)

    # ✅ Build kiến trúc mạng
    model.build()

    # ✅ Nếu có trọng số, load chúng (tùy vào thư mục của bạn)
    try:
        if model.load_latest_model():
            print("✅ Loaded latest model.")
        else:
            print("⚠️ No latest model found, using freshly built model.")
    except Exception as e:
        print("⚠️ Could not load weights:", e)

    # ✅ Khởi động API
    api = ChessModelAPI(agent_model=model)
    api.start()

    print("✅ ChessModelAPI started successfully.")
