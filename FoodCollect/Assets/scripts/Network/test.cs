    using System.Collections.Generic;
    
    [System.Serializable]
    public class Datum
    {
        public List<int> Floor;
        public List<int> AgentPositions;
    }

    [System.Serializable]
    public class ModelResponse
    {
        // Define the structure of response data
        public int steps;
        public List<Datum> data;

    }