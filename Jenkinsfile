pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh '''
                    ls -l
                    echo "second step"
                '''
            }
            
        }
    }
}

