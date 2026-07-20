import threading
class BackgroundWorker:
 def __init__(self,logger):self.logger=logger;self.thread=None
 def start(self,task,success,failure):
  if self.thread and self.thread.is_alive():return
  def run():
   try:success(task())
   except BaseException as x:self.logger.exception("Worker failure");failure(x)
  self.thread=threading.Thread(target=run,name="A2LParserWorker",daemon=True);self.thread.start()
