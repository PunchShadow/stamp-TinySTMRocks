#ifndef _PARAM_H_
#define _PARAM_H_

#ifdef CT_TABLE
# define TOTAL_CONTEXT_NUM                  15 /* TODO: Auto set by the maximum transactions correspoding to application */
# define MAX_ENTRY_SIZE                      9 /* The maximum number of pending tasks in the same time */
#endif /* CT_TABLE */

#ifdef CONTENTION_INTENSITY
# define ci_alpha                           0.449     /* TODO: hyper-parameter of alpha */
# define CI_THRESHOLD                       0.651 /* FIXME: Find a proper */
#endif /* CONTENTION_INTENSITY */



/* Scheduling Policy 0: randomo select, 1: ACO */
#define SCHEDULE_POLICY                     1


#endif /* _PARAM_H_ */