// Here we declare that we're developing a pipeline for Jenkins 
pipeline{ 

    // Here we define the agents (the connected machines) on which to run the pipeline 
    agent any

    // Here we define the different cycles of pipeline, depending on their purpose 
    stages{
        stage("build"){

            steps{
                echo "Building the application..."
            }
        }

        stage("test")
            steps{
                echo "Testing the application..."
            }
        }
        
        stage("deploy"){
            steps{
                echo "Deploying the application..."
            }
        }

}
