// constants
const SAMPLING_PERIOD 10ms;
const COMMAND_EVENT_DETECTED 1;
const COMMAND_REQUEST_DATA 2;
// the data collection interval after event detection (one minute)
const DATA_COLLECTION_INTERVAL 60s;
// coefficients for exponentially weighted moving average
const EWMA_COEFF_1_NUMERATOR 15;
const EWMA_COEFF_1_DENOMINATOR 100;
const EWMA_COEFF_2_NUMERATOR 7;
const EWMA_COEFF_2_DENOMINATOR 34;
const EVENT_DETECTION_THRESHOLD 0x1234;

// sample acoustic and seismic sensors
read AcousticSensor, period SAMPLING_PERIOD;
read SeismicSensor, period SAMPLING_PERIOD;
Output File (AcousticSensor, SeismicSensor, Timestamp), filename "SensorData.bin";

// event is detected when the difference between two EWMA becomes large enough
define CombinedSensor sum(AcousticSensor, SeismicSensor); // just something that combines both
define EventDetectionFunction difference(
         EWMA(CombinedSensor, EWMA_COEFF_1_NUMERATOR, EWMA_COEFF_1_DENOMINATOR),
         EWMA(CombinedSensor, EWMA_COEFF_2_NUMERATOR, EWMA_COEFF_2_DENOMINATOR));
when EventDetectionFunction > EVENT_DETECTION_THRESHOLD:
    // event detected (locally), send info to base station
    // (timestamp is appended automatically)
    output Network (Command), command COMMAND_EVENT_DETECTED;
end;

// check for data query command
NetworkRead RemoteCommand(Command, Timestamp);
when RemoteCommand.Command == COMMAND_REQUEST_DATA:
    // collect all data that was read in interval [Timestamp, Timestamp + 60]
    Output Network, file "SensorData.bin",
        where 
            RemoteCommand.Timestamp >= Timestamp
            and RemoteCommand.Timestamp <= add(Timestamp, DATA_COLLECTION_INTERVAL);
end