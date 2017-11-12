#include <unistd.h>
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  
#define loop_index 100
#define refresh_interval 30
int main(void) {

      int i;
      char **p=(char**)malloc(loop_index*sizeof(char*));
      int malloc_size = 46.5 * (1 << 20);      
      /* intro message */
      printf("Starting ...\n");
      while(1){
      /* loop 50 times, try and consume 50 MB of memory */
      for (i = 0; i < loop_index; ++i) {

          /* failure to allocate memo*/
	if ((*(p+i) = malloc(malloc_size)) == NULL) {
              printf("Malloc failed at %d MB\n", i);
              return 0;
	}
	sleep(0.03 * i);
          /* take memory and tell user where we are at */
	memset(*(p+i), 0, (malloc_size));
          // printf("Allocated %d to %d MB\n", i, i+1);

      }

      /* exit message and return */
      printf("Done!\n");
      sleep(refresh_interval);
      for (i=0;i<loop_index;i++){
	free(*(p+i));
        if(i < 30) {sleep(0.03 * i);}
	// printf("Free %d to %d MB\n", i, i+1);
      }
	break;	
      }
      return 0;

  }

