#include <unistd.h>
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  
#define loop_index 100
#define refresh_interval 2
int main(void) {

      int i;
      char **p=(char**)malloc(loop_index*sizeof(char*));
      
      /* intro message */
      printf("Starting ...\n");
      while(1){
      /* loop 50 times, try and consume 50 MB of memory */
      for (i = 0; i < loop_index; ++i) {

          /* failure to allocate memo*/
	if ((*(p+i) = malloc(1<<20)) == NULL) {
              printf("Malloc failed at %d MB\n", i);
              return 0;
	}

          /* take memory and tell user where we are at */
	memset(*(p+i), 0, (1<<20));
          printf("Allocated %d to %d MB\n", i, i+1);

      }

      /* exit message and return */
      printf("Done!\n");
      sleep(refresh_interval);
      for (i=0;i<loop_index;i++){
	free(*(p+i));
        printf("Free %d to %d MB\n", i, i+1);
      }
      }
      return 0;

  }

