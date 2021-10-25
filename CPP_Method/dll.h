#ifndef _DLL_H_
#define _DLL_H_

#if BUILDING_DLL
#define DLLIMPORT __declspec(dllexport)
#else
#define DLLIMPORT __declspec(dllimport)
#endif

extern "C" DLLIMPORT void method_03(double inArray[], unsigned int size,double outArray[],double param[])  ;

extern "C" DLLIMPORT int method_02(int a,int b) ;
//extern "C" DLLIMPORT char* hello();

/*
class DLLIMPORT DllClass
{
	public:
		DllClass();
		virtual ~DllClass();
		void HelloWorld();
};
*/
#endif

