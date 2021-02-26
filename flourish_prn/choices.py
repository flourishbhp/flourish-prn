from edc_constants.constants import OTHER


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
     'Enrolled erroneously – did not meet eligibility criteria'),
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

OFFSTUDY_POINT = (
    ('prior_to_del', 'Prior to Delivery'),
    ('post_del', 'Post Delivery'),
)
