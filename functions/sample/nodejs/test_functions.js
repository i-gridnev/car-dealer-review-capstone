/**
 * Get all databases
 */

const {main} = require('./get_dealers_with_filters.js');
var creds = require('../../.creds.json');

main({
    apikey : creds.apikey,
    url : creds.url,
    state: 'TX'
    }).then(data => 
        console.log(data)
        );