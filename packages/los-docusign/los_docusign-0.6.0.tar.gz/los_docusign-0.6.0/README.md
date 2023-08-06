# Django-DocuSign
Django wrapper app for DocuSign functionalities

`pip install django-docusign`

## Running Tests
We have a unit test defined for testing the los application.
This can be executed using the below command.

```
python manage.py test
```

## Usage
In order to use the system you must add los_docusign.apps.LosDocusignConfig to your installed apps in your settings.py file.
```python
INSTALLED_APPS = [
    'los_docusign'
]
```

Test file has the sample implementation of the test_app

## Functions in client.py
1.  generate_docusign_preview_url(dict)

    Params required in dict:
    -   "envelope_id"
    -   "authentication_method"
    -   "email"
    -   "user_name"
    -   "client_user_id"
    -   "return_url"

2. create_envelope(payload)

    Params required:
    -   DocuSign payload in JSON format

3. download_docusign_document(dict)

    Params required in dict:
    -   "envelope_id"
    -   "doc_download_option"
        -   Valid Values:
            1. archive - If the document to be downloaded in zip format.
            2. combined - If the document to be downloaded as a combined document.

4. process_docusign_webhook(xml_string)

    Params required:
    -   Webhook XML string received from Docusign.

    Response dict:
        {
            "envelopeId": "c57ec066-c5fa-4aa0-873d-6f285d70242a",
            "envelope_status": "sent",
            "recipients": [
                {
                    "recipient_id": "a7f73f21-c4ff-4bcb-97c4-b03c91b8528a",
                    "email": "test@test.com",
                    "name": "John Nash",
                    "status": "autoresponded"
                },
                {
                    "recipient_id": "511b2ad3-6650-4773-a6b4-47f64a0ccdaf",
                    "email": "jerry@test.com",
                    "name": "Jerry Tunes",
                    "status": "created"
                },
                {
                    "recipient_id": "0851505f-5af2-42df-bce4-9e0ebe8bd2e2",
                    "email": "tom@test.com",
                    "name": "Tom Tunes",
                    "status": "created"
                }
            ]
        }

5. update_envelope_and_resend(envelope_id, signers_data)
This function is used to update the email/phone number of the signer.
This is also used to resend the same envelope to the signers. For resending, recipientId and email are mandatory.

    Params required:
    -   envelope_id - The envelope id for which we need to update the signers information or send the same envelope to the signers.
    -   signers_data - The signer array which has the information about the signers that needs to be updated.
    Params required in signers_data:
    -   email - The email of the signer.
    -   recipientId - The recipient id of the signer
    -   phone  - The phone number of the signer (optional)

    signers_data example:
    [
        {
            "recipientId":"123456",
            "email":"test@test.com",
            "phone":"1234567890"
        }
    ]

5. update_envelope_status(status_info):
This function is used to update the status of the envelope.

    Params required:
    -   status_info - The dictionary variale which has the following parameters.
        - envelope_id - The envelope id for which the status needs to be updated
        - status - The status in which we need to set the envelope
        - reason - The reason (if applicable) to be set for the status change. This will be visible to the signer

    status_info example:
    {
        "envelope_id":"b1435c5d-3d67-46e8-ab6a-54789f42924e",
        "status":"voided",
        "reason":"Voiding an envelope"
    }
    
