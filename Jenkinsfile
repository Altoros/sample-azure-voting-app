podTemplate(
        label: "azure-vote-app",
        cloud: "kubernetes",
        containers: [
                containerTemplate(name: "python", image: "python:3", ttyEnabled: true, command: "cat"),
                containerTemplate(name: 'docker', image: 'docker:19.03.1', command: 'cat', ttyEnabled: true)
        ],

        volumes: [
                hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock'),
        ]
) {
    properties([
            parameters([
                    string(name: 'REGISTRY_URL', defaultValue: 'voteapptest.azurecr.io'),
                    string(name: 'REPO', defaultValue: 'https://github.com/Altoros/sample-azure-voting-app.git'),
                    string(name: 'BRANCH', defaultValue: 'main'),
                    string(name: 'TAG', defaultValue: 'latest')
            ])
    ])

    def app_frontend = 'azure-vote'
    def app_backend = 'azure-vote-mysql'

    TAG = "${env.BUILD_ID}"

    node("azure-vote-app") {
        stage('Fetch Source') {
            git branch: "${params.BRANCH}", url: "${params.REPO}"
        }

        container("python") {
            withEnv([
                    'MYSQL_USER=fakeuser',
                    'MYSQL_PASSWORD=fakepass',
                    'MYSQL_DATABASE=fakedb',
                    'MYSQL_HOST=localhost'
            ]) {
                stage("Run Tests") {
                    dir ("./${app_frontend}/azure-vote"){
                        sh 'pip install -r requirements.txt'
                        sh 'pytest'
                    }
                }
            }
        }

        container("docker") {
            stage("Build Image") {
                dir ("./${app_frontend}"){
                    sh 'echo Build App Frontend Image'
                    sh """docker build -t ${params.REGISTRY_URL}/$app_frontend:${TAG} ."""
                }
                dir ("./${app_backend}"){
                    sh 'echo Build App Backend Image'
                    sh """docker build -t ${params.REGISTRY_URL}/$app_backend:${TAG} ."""
                }
            }

            stage("Push Image") {
                withCredentials([usernamePassword(
                        credentialsId: "azure-container-registry-creds",
                        usernameVariable: "USER",
                        passwordVariable: "PASS"
                )]) {
                    sh """docker login -u $USER -p $PASS ${params.REGISTRY_URL}"""

                    sh """docker push ${params.REGISTRY_URL}/$app_frontend:${TAG}"""
                    sh """docker push ${params.REGISTRY_URL}/$app_backend:${TAG}"""

                }
            }
        }
    }
}