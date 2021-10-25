/* Replace "dll.h" with the name of your header */
#include "dll.h"
//#include <windows.h>
/*
DllClass::DllClass()
{

}

DllClass::~DllClass()
{

}
*/
DLLIMPORT void method_03(double inArray[], unsigned int size,double outArray[],double param[])  //²ßºD·LÄé
{
	float res =inArray[0];
	float buff_res = res ;
	float gres = res;
	float sub_res;
	double *ppt,*spt;
	ppt = &inArray[0];
	spt = &outArray[0];
	
  for(int i =0;i<size;i++)
  {
	res = (res*param[0] + *ppt) / (param[0]+1 );
	gres = (gres*param[1] + *ppt++) / (param[1]+1 );
	sub_res = res-gres;
	
	buff_res = (buff_res*param[2] + sub_res) /(param[2]+1 );
	*spt++ = buff_res;
  }
}

DLLIMPORT int method_02(int a,int b) 
{
	return (a+b);
}
/*
DLLIMPORT char* hello()
{
	
	return "Hello";
}
*/
/*
void DllClass::HelloWorld()
{
	MessageBox(0, "Hello World from DLL!\n","Hi",MB_ICONINFORMATION);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason,LPVOID lpvReserved)
{
	switch(fdwReason)
	{
		case DLL_PROCESS_ATTACH:
		{
			break;
		}
		case DLL_PROCESS_DETACH:
		{
			break;
		}
		case DLL_THREAD_ATTACH:
		{
			break;
		}
		case DLL_THREAD_DETACH:
		{
			break;
		}
	}
	
	
	return TRUE;
}
*/

