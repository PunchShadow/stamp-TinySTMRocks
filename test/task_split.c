#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>

#include "tm.h"
#include "thread.h"

typedef struct data {
    int int_var;
    char char_var;
} data_t;

typedef struct task {
    int num;
    void* data;
} task_t;

typedef struct createTask {
    int times;
} createTask;


void
thread_work(void* argPtr)
{
    TM_THREAD_ENTER();
    printf("Enter thread_work!!!!!\n");
    while(1) {
        hs_task_t* Ptr = TM_TaskPop(0);
        if (Ptr == NULL) {
            break;
        }
        task_t* taskPtr = (task_t*)Ptr->data;
        data_t* dataPtr = (data_t*)taskPtr->data;
        printf("[t_id:%d][data->int:%d][data->char:%c]\n", taskPtr->num, dataPtr->int_var, dataPtr->char_var);
    }

    TM_THREAD_EXIT();
}


data_t*
create_data(int int_var, char char_var)
{
    data_t* dataPtr = malloc(sizeof(data_t));
    dataPtr->int_var = int_var;
    dataPtr->char_var = char_var;
    return dataPtr;
}

task_t*
create_task(int task_num, void* data)
{
    task_t* taskPtr = malloc(sizeof(task_t));
    taskPtr->num = task_num;
    taskPtr->data = data;
    return taskPtr;
}


MAIN(argc, argv)
{
    GOTO_REAL();

    int numThread = 1;
    SIM_GET_NUM_CPU(numThread);
    TM_STARTUP(numThread);
    P_MEMORY_STARTUP(numThread);
    thread_startup(numThread);

    /* Build up the tasks */
    for(int i=0; i < 100; i++) {
        data_t* dataPtr = create_data(i, 'a');
        void* taskPtr = (void*)create_task(i*10, (void*)dataPtr);
        TM_TaskSplit(taskPtr, 0);
    }

    thread_start(&thread_work, NULL);



    TM_SHUTDOWN();
    P_MEMORY_SHUTDOWN();

    GOTO_SIM();

    thread_shutdown();

    MAIN_RETURN(0);
}