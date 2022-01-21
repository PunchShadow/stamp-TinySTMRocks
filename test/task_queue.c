#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>

#include "tm.h"
#include "thread.h"



typedef struct task {
    int data;
} task_t;

typedef struct createTask {
    int times;
} createTask;


static void
createTaskList(void* argPtr)
{
    TM_THREAD_ENTER();
    pthread_t thread_id = pthread_self();

    createTask* createTaskPtr = (createTask*)argPtr;
    int times = createTaskPtr->times;

    for (int i = 0 ; i < times; i++) {
        task_t* taskPtr;
        taskPtr = malloc(sizeof(task_t));
        taskPtr->data = (i);
        //printf("%lu: Create %d\n", thread_id, taskPtr->data);
        TM_TaskPush(taskPtr, 0);
    }
    

    TM_THREAD_EXIT();    
}

static void
consumeTaskList(void* argPtr)
{
    TM_THREAD_ENTER();
    pthread_t thread_id = pthread_self();
    while(1) {
        task_t* taskPtr;
        taskPtr = TM_TaskPop(0);
        if (taskPtr == NULL) {
            printf("GOING TO BREAK");
            break;
        }

        int data = taskPtr->data;
        //printf("%lu, Consume %d\n", thread_id, data);
        if (data%2) {
            task_t* taskPtr;
            taskPtr = malloc(sizeof(task_t));
            taskPtr->data = (data+3);
            TM_TaskPush(taskPtr,0);
            printf("%lu, Push %d\n", thread_id, taskPtr->data);
        }
    }
    printf("%lu Thread finish !!!!!!\n", thread_id);
    TM_THREAD_EXIT();
}




MAIN(argc, argv)
{
    GOTO_REAL();

    int numThread = 2;
    SIM_GET_NUM_CPU(numThread);
    TM_STARTUP(numThread);
    P_MEMORY_STARTUP(numThread);
    thread_startup(numThread);


    /* Build up the tasks */
    createTask* createTaskPtr;
    createTaskPtr = malloc(sizeof(createTask));
    createTaskPtr->times = 10;

    thread_start(&createTaskList, (void*)createTaskPtr);
    thread_start(&consumeTaskList, (void*)createTaskPtr);


    TM_SHUTDOWN();
    P_MEMORY_SHUTDOWN();

    GOTO_SIM();

    thread_shutdown();

    MAIN_RETURN(0);
}