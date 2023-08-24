# Send email by webhook trigger

This program runs Python Flask to listen for a webhook call and send notification emails. Currently, it is catering to single use case as per my lab setup, but it can be extended as and when needed.

It is currently deployed by running this script as a service on an Ubuntu server. The main purpose is to listen for an error notification from one of our security solutions called Cribl, and send an automated email with the required details to the solution admin for further analysis.

The basic flow of this use case is:
Security Solution runs into error -> Sends error via webhook to our program -> Our script receives recipient email as header and error details as body -> Send an email via SMTP -> Return status (sent successfully or error sending emails and reason) 