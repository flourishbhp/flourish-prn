from edc_constants.constants import OTHER


CAUSE_OF_DEATH_CAT = (
    ('hiv_related', 'HIV infection or HIV related diagnosis'),
    ('hiv_unrelated', 'Disease unrelated to HIV'),
    ('study_drug', 'Toxicity from Study Drug'),
    ('non_study_drug', 'Toxicity from non-Study drug'),
    ('trauma', 'Trauma/Accident'),
    ('no_info', 'No information available'),
    (OTHER, 'Other, specify'),)

CAREGIVER_OFF_STUDY_REASON = (
    ('multiple_vialble_gestations',
     'Multiple (2 or more) viable gestations seen on ultrasound'),
    ('unable_to_determine_ga', 'Unable to confirm GA by Ultrasound.'),
    ('miscarriage_or_arbotion',
     'Miscarriage or abortion'),
    ('fetal_death_gt_20wks',
     'fetal Death at >= 20weeks GA (IUFD) or still born'),
    ('took_art_less_than_4weeks',
     'Biological mother took ART for less than 4 weeks during pregnancy'),
    ('caregiver_death',
     'Caregiver death (complete the Death Report Form AF005)'),
    ('moving_out_of_study_area',
     'Participant stated that they will be moving out of the study area or '
     'unable to stay in study area'),
    ('loss_to_followup',
     'Participant lost to follow-up/unable to locate'),
    ('loss_to_followup_contacted',
     'Participant lost to follow-up, contacted but did not come to study '
     'clinic'),
    ('caregiver_withdrew_consent',
     'Caregiver changed mind and withdrew consent'),
    ('father_refused',
     'Father of the infant/child/adolescent refused to participate and therefore'
     ' participant withdrew consent '),
    ('family_member_refused',
     'Other family member refused the study and therefore participant withdrew '
     'consent'),
    ('caregiver_hiv_infected',
     'Caregiver was found to be HIV-infected and the date of infection cannot '
     'be determined prior to the birth of their child'),
    ('infant_hiv_infected',
     'Infant/Child/Adolescent found to be HIV-infected'),
    ('infant_death',
     'Infant/Child/Adolescent death (complete Infant Death Report Form)'),
    ('protocol_completion',
     'Completion of protocol required period of time for observation '
     '(see Study Protocol for definition of "Completion") (skip to end of form)'),
    ('enrolled_erroneously',
     'Enrolled erroneously – did not meet eligibility criteria prior to consent prior to consent'),
     ('Did not meet eligibility criteria, after consent obtained'),
    ('incarcerated',
     'Participant is incarcerated'),
    (OTHER, 'Other'),
)

CHILD_OFF_STUDY_REASON = (
    ('moving',
     'Participant stated she will be moving out of the study area or unable to'
     ' stay in study area'),
    ('ltfu', 'Participant lost to follow-up/ unable to locate'),
    ('lost_no_contact',
     'Participant lost to follow-up, contacted but did not come to study clinic'),
    ('child_withdrew', 'Child/Adolescent changed mind and withdrew consent'),
    ('withdrew_by_father',
     'Father of the infant/child/adolescent refused to participate and therefore'
     ' participant withdrew consent'),
    ('withdrew_by_family',
     'Other family member refused the study and therefore participant withdrew'
     ' consent '),
    ('hiv_pos', 'Infant/child/adolescent found to be HIV-infected'),
    ('death',
     ('Infant/child/adolescent Death (complete the Infant Death Report Form)')),
    ('complete',
     (' Completion of protocol required period of time for observation'
      ' (see Study Protocol for definition of Completion.)'
      ' [skip to end of form]')),
    ('incarcerated', 'Adolescent is incarcerated'),
    (OTHER, ' Other'),
)

HOSPITILIZATION_REASONS = (
    ('respiratory illness(unspecified)', 'Respiratory Illness(unspecified)'),
    ('respiratory illness, cxr confirmed',
     'Respiratory Illness, CXR confirmed'),
    ('respiratory illness, cxr confirmed, bacterial pathogen, specify',
     'Respiratory Illness, CXR confirmed, bacterial pathogen, specify'),
    ('respiratory illness, cxr confirmed, tb or probable tb',
     'Respiratory Illness, CXR confirmed, TB or probable TB'),
    ('diarrhea illness(unspecified)', 'Diarrhea Illness(unspecified)'),
    ('diarrhea illness, viral or bacterial pathogen, specify',
     'Diarrhea Illness, viral or bacterial pathogen, specify'),
    ('sepsis(unspecified)', 'Sepsis(unspecified)'),
    ('sepsis, pathogen specified, specify',
     'Sepsis, pathogen specified, specify'),
    ('mengitis(unspecified)', 'Mengitis(unspecified)'),
    ('mengitis, pathogen specified, specify',
     'Mengitis, pathogen specified, specify'),
    ('non-infectious reason for hospitalization, specify',
     'Non-infectious reason for hospitalization, specify'),
    (OTHER, 'Other infection, specify'),
)

MED_RESPONSIBILITY = (
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse'),
    ('traditional', 'Traditional Healer'),
    ('all', 'Both Doctor or Nurse and Traditional Healer'),
    ('none', 'No known medical care received (family/friends only)'),)

OFFSTUDY_POINT = (
    ('prior_to_del', 'Prior to Delivery'),
    ('post_del', 'Post Delivery'),
)

RELATIONSHIP_CHOICES = (
    ('not_related', 'Not related'),
    ('probably_not_related', 'Probably not related'),
    ('possibly_related', 'Possibly related'),
    ('probably_related', 'Probably related'),
    ('definitely_related', 'Definitely related'),
)

SOURCE_OF_DEATH_INFO = (
    ('autopsy', 'Autopsy'),
    ('clinical_records', 'Clinical_records'),
    ('study_staff',
     'Information from study care taker staff prior participant death'),
    ('health_care_provider',
     'Contact with other (non-study) physician/nurse/other health care provider'),
    ('death_certificate', 'Death Certificate'),
    ('relatives_friends',
     'Information from participant\'s relatives or friends'),
    ('obituary', 'Obituary'),
    ('pending_information', 'Information requested, still pending'),
    ('no_info', 'No information will ever be available'),
    (OTHER, 'Other, specify'),)
