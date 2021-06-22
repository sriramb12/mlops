# Software Requirements for MLMS (derived from SRS document)

## Following Assumptions
  * An RDBMS will be used to store data
 
 Mostly TBD 

## Functional requirements

 * Run as a background service 
 * Input is specified in JSON formatted files
 * Initialize runtime parameters 
    - periodicity 
    - port numbers for various subservices (maybe just 1 port will do)
    - access points (RESTful endpoints)
    - log file location
 * Initialize using a set of predefined input files (JSON format) to instantiate and monitor models (running as applications)
 * Discover all deployed ML algorithms
 * Monitor all deployed ML algorithms
 * Handle exceptions
 * Perform corrective actions
 * Concurrency in monitoring

