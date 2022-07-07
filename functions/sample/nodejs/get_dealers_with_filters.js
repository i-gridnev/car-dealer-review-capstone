/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main({ apikey, url, state, dealerId }) {
    try {
        const authenticator = new IamAuthenticator({ apikey })
        const cloudant = CloudantV1.newInstance({ authenticator });
        cloudant.setServiceUrl(url);

        const dbName = 'dealerships';
        const fields = ['id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long', 'full_name', 'short_name'];
        
        let selector;
        if (dealerId){
            selector = { id: {'$eq': parseInt(dealerId)} };
        } else if (state){
            selector = { st: {'$eq': state} };
        } else {
            selector = { st: {'$exists': true} };
        } 
        
        let docs = await cloudant.postFind( {db: dbName, selector: selector, fields: fields} );
        const dealers = docs.result['docs']
        if (!dealers.length) {
            return { 
                statusCode: 404,
                message: 'the database is empty'
            };
        }
        return { 
            statusCode: 200,
            dealers: dealers,
        };
    } catch (error) {
        return { 
            statusCode: 500, 
            message: 'something went wrong on the server' 
        };    
    }
  }
exports.main = main