// Source: https://www.youtube.com/watch?v=7KCS70sCoK0

// This is a global variable that we define and we link it to a custom Groovy function that should check for code changes
// CODE_CHANGES = getGitChanges()

// This is a local variable that we define and we link it to a custom Groovy function
def groovyScript

// Here we declare that we're developing a pipeline for Jenkins 
pipeline{ 

    // Here we define the agents (the connected machines) on which to run the pipeline 
    agent any

    // This section allows us to accept parameters which are to be used within the pipeline
    // For example, some external configuration for the version of the App that is to be deployed 
    parameters{
        choice(name: 'VERSION', choices: ['1.0', '1.1', '1.2'], description: "Description not available yet")
        booleanParam(name: 'executeTests', defaultValue: true, description: "Description not available yet")
    }

    // Here we define which tools can be used in the project. They are limited to Maven, Gradle and JDK 
    /*tools{
        maven Maven
    }*/

    environment{
        // This is an environmental variable that we define 
        NEW_VERSION = '1.3.0'
        // This variable is provided a Jenkins plugin named 'Credentials Binding'
        // It takes the ID of the credentials as a parameter
        SERVER_CREDENTIALS = credentials('PyWebApp-Credentials')
    }

    // Here we define the different cycles of pipeline, depending on their purpose 
    stages{

        stage("init"){
            steps{
                script{
                    groovyScript = load "script.groovy"
                }
            }
        }


        stage("build"){
            steps{
                // Here we import the 'buildApp()' function from the script.groovy file and then run it 
                script{
                    groovyScript.buildApp()
                }
            }
        }

        stage("test"){
            // This section defines when the 'test' Build stage should be completed 
            when{
                // This expression section allows us to place conditions on when certain tasks should be done 
                expression {
                    // This is an environment variable that Jenkins automatically provides 
                    // All available environmental variables are here listed within Jenkins, here: http://139.162.146.107:8080/env-vars.html/
                    env.BRANCH_NAME == "dev-v1*" && params.executeTests == true
                }
            }
            steps{
                script{
                    groovyScript.testApp()
                }
            }
        }
        
        stage("deploy"){
            steps{
                echo "Deploying the application..."
                // Here we use a plugin to bind the credentials stored within Jenkins to local variables 
                // Source: https://www.jenkins.io/doc/pipeline/steps/credentials-binding/
                // Copies the SSH key file given in the credentials to a temporary location, then sets a variable to that location - the file is deleted when the build completes.
                withCredentials([
                    sshUserPrivateKey(credentialsId: 'PyWebApp-Credentials', keyFileVariable: '/tmp/key-deleteme')
                ]){
                    sh "echo 'Deploying the app with credentials stored within Jenkins'" 
                }
                // IMPORTANT: Similarly to Bash, in order to expand a string we must use double quotes
                script{
                    groovyScript.deployApp()
                }
            }
        }
    }
    // All code within this section will be executed once all stages have been executed
    post{
        // This section will be executed always - no matter whether the build failed or succeeded 
        always {
            echo "The Build was successfull!"
        }
        // This section will be executed only if the Build fails
        failure{
            echo "The Build was not successful!"
        }

    }
}

