# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/utils/notify.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 9092 bytes
import logging
from flask_mail import Message
LOG = logging.getLogger(__name__)

def notify_match_internal(database, match_obj, admin_email, mail, notify_complete):
    """Send an email to patient contacts after an internal match

    Args:
        database(pymongo.database.Database): patientMatcher database
        match_obj(dict): an object containing both query patient(dict) and matching results(list)
        admin_email(str): email of the server admin
        mail(flask_mail.Mail): an email instance
        notify_complete(bool): set to False to NOT notify variants and phenotype terms by email
    """
    sender = admin_email
    patient_id = None
    patient_label = None
    results = None
    recipient = None
    email_subject = 'MatchMaker Exchange: new patient match available.'
    email_body = None
    internal_patient = database['patients'].find_one({'_id': match_obj['data']['patient']['id']})
    if internal_patient:
        patient_id = match_obj['data']['patient']['id']
        patient_label = match_obj['data']['patient'].get('label')
        recipient = match_obj['data']['patient']['contact']['href'][7:]
        email_body = active_match_email_body(patient_id=patient_id, match_results=(match_obj['results']), patient_label=patient_label, external_match=False,
          notify_complete=notify_complete)
        LOG.info('Sending an internal match notification for query patient with ID:{0}. Patient contact: {1}'.format(patient_id, recipient))
        kwargs = dict(subject=email_subject, html=email_body, sender=sender, recipients=[recipient])
        message = Message(**kwargs)
        try:
            mail.send(message)
        except Exception as err:
            LOG.error('An error occurred while sending an internal match notification: {}'.format(err))

    for result in match_obj['results'][0]['patients']:
        patient_id = result['patient']['id']
        if internal_patient:
            if internal_patient['_id'] == patient_id:
                continue
        patient_label = result['patient'].get('label')
        recipient = result['patient']['contact']['href'][7:]
        email_body = passive_match_email_body(patient_id, match_obj['data']['patient'], patient_label, notify_complete)
        LOG.info('Sending an internal match notification for match result with ID {}'.format(patient_id))
        kwargs = dict(subject=email_subject, html=email_body, sender=sender, recipients=[recipient])
        message = Message(**kwargs)
        try:
            mail.send(message)
        except Exception as err:
            LOG.error('An error occurred while sending an internal match notification: {}'.format(err))


def notify_match_external(match_obj, admin_email, mail, notify_complete):
    """Send an email to patients contacts to notify a match on external nodes

    Args:
        match_obj(dict): an object containing both query patient(dict) and matching results(list)
        admin_email(str): email of the server admin
        mail(flask_mail.Mail): an email instance
        notify_complete(bool): set to False to NOT notify variants and phenotype terms by email
    """
    sender = admin_email
    patient_id = match_obj['data']['patient']['id']
    patient_label = match_obj['data']['patient'].get('label')
    recipient = match_obj['data']['patient']['contact']['href'][7:]
    email_subject = 'MatchMaker Exchange: new patient match available.'
    email_body = active_match_email_body(patient_id=patient_id, match_results=(match_obj['results']), patient_label=patient_label, external_match=True,
      notify_complete=notify_complete)
    LOG.info('Sending an external match notification for query patient with ID {0}. Patient contact: {1}'.format(patient_id, recipient))
    kwargs = dict(subject=email_subject, html=email_body, sender=sender, recipients=[recipient])
    message = Message(**kwargs)
    try:
        mail.send(message)
    except Exception as err:
        LOG.error('An error occurred while sending an external match notification: {}'.format(err))


def active_match_email_body(patient_id, match_results, patient_label=None, external_match=False, notify_complete=False):
    """Returns the body message of the notification email when the patient was used as query patient

    Args:
        patient_id(str): the ID of the patient submitted by the  MME user which will be notified
        match_results(list): a list of patients which match with the patient whose contact is going to be notified
        external_match(bool): True == match in connected nodes, False == match with other patients in database
        patient_label(str): the label of the patient submitted by the  MME user which will be notified (not mandatory field)
        notify_complete(bool): set to False to NOT notify variants and phenotype terms by email

    Returns:
        html(str): the body message
    """
    search_type = 'against the internal database of MatchMaker patients'
    if external_match:
        search_type = 'against external nodes connected to MatchMaker'
    html = "\n        ***This is an automated message, please do not reply to this email.***<br><br>\n        <strong>MatchMaker Exchange patient matching notification:</strong><br><br>\n        Patient with ID <strong>{0}</strong>, label <strong>{1}</strong>.\n        This search returned these potential matches</strong>:<br>\n        <strong>{2}</strong><br>\n        You might directly contact the matching part using the address specified in patient's data or review matching\n        results in the portal you used to submit your patient.\n        <br><br>\n        Kind regards,<br>\n        The PatientMatcher team\n    ".format(patient_id, patient_label, html_format(match_results, 0, notify_complete))
    return html


def passive_match_email_body(patient_id, matched_patient, patient_label=None, notify_complete=False):
    """Returns the body message of the notification email when the patient was used as query patient

    Args:
        patient_id(str): the ID of the patient submitted by the MME user which will be notified
        matched_patient(dict): a patient object
        patient_label(str): the label of the patient submitted by the  MME user which will be notified (not mandatory field)
        notify_complete(bool): set to False to NOT notify variants and phenotype terms by email

    Returns:
        html(str): the body message
    """
    html = "\n        ***This is an automated message, please do not reply.***<br>\n        <strong>MatchMaker Exchange patient matching notification:</strong><br><br>\n        Patient with <strong>ID {0}</strong>,<strong> label {1}</strong> was recently returned as a match result\n        in a search performed using a patient with these specifications:<br>\n        <strong>{2}</strong><br>\n        You might directly contact the matching part using the address specified in patient's data or review matching\n        results in the portal you used to submit your patient.\n        <br><br>\n        Kind regards,<br>\n        The PatientMatcher team\n    ".format(patient_id, patient_label, html_format(matched_patient, 0, notify_complete))
    return html


def html_format(obj, indent=0, notify_complete=False):
    """Formats one or more patient objects to a nice html string

    Args:
        obj(list): a list of patient objects or a patient object
        notify_complete(bool): set to False to NOT notify variants and phenotype terms by email
    """
    if isinstance(obj, list):
        htmls = []
        for k in obj:
            htmls.append(html_format(obj=k, indent=(indent + 1), notify_complete=notify_complete))

        return '[<div style="margin-left: %dem">%s</div>]' % (indent, ',<br>'.join(htmls))
    else:
        if isinstance(obj, dict):
            htmls = []
            for k, v in obj.items():
                if notify_complete or k in ('node', 'patients', 'patient', 'contact',
                                            'id', 'name', 'href', 'institution'):
                    htmls.append("<span style='font-style: italic; color: #888'>%s</span>: %s" % (k,
                     html_format(obj=v, indent=(indent + 1), notify_complete=notify_complete)))

            return '{<div style="margin-left: %dem">%s</div>}' % (indent, ',<br>'.join(htmls))
        return str(obj)