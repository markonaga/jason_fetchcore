// run this on page load and on a timeout


const FetchcoreClient = require('fetchcore-sdk').FetchcoreClient;

const hostname = 'im2.fetchcore-cloud.com';
const port = 8000;
const client = FetchcoreClient.defaultClient();
const enableSSL = false;

function connectClient() {
	client.configure(hostname, port, enableSSL);
	client.authenticate('jvranek@innovation-matrix.com', 'innovation')
    .then(() => {
        console.log("yippeee")
    })
    .catch((clientError) => {
        console.log("Failed to connect, check login details")
    });
}

