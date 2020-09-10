using System.Threading;

namespace VR
{
    public abstract class RunAbleThread
    {
        private readonly Thread _runnerThread;

        protected RunAbleThread()
        {
            _runnerThread = new Thread(Run);
        }

        protected bool Running { get; private set; }

        protected abstract void Run();

        public void Start()
        {
            Running = true;
            _runnerThread.Start();
        }

        public void Stop()
        {
            Running = false;
            _runnerThread.Join();
        }
    }
}