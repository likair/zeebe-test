# QA Test engineer assignment

In this assignment the applicant should come up with a method to make sure the system in question is responsive. In other words, study references and based on them, implement automated test(s) to verify system gives a response.

System under test is the Zeebe workflow engine [GitHub](https://github.com/camunda/zeebe). To test it, system must be running and this can be done for example by deploying it in localhost.


## Requirements and expectations

* Create automated test(s) to run against system under testing to verify system gives a response which may be a positive or a negative response. Assignment should contain
  * short description of how system is tested
  * chosen technologies, libraries and dependencies
  * implementation of automated test(s) and final report of a successful run of test(s)
  * instructions how to run test(s)

Target of test(s) can be any component or part of the system which is running after successful deployment. Your test may for example verify Zeebe gateway health status. The very purpose of this assignment is to provide a working solution, prepare to explain the basic idea of test(s) in technical interview and answer related questions.


## Instructions

Study also https://docs.camunda.io/docs/1.1/components/zeebe/zeebe-overview/ and related documentation. To deploy the system, you may use Docker (https://docs.docker.com/) or any other container orchestration you prefer. You can target the system with test from outside or inside container. If you want to use Zeebe health checks in your assignment, you need to tell container to specifically publish those services if you want to access them outside container. Depending on test platform, it may be useful to run container with Zeebe standalone gateway to take advantage of it in testing.