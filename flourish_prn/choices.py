from edc_constants.constants import OTHER

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
