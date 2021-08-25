
#ifndef Application_H
#define Application_H

#include "basicTypes.h"
#include "mpi.h"

namespace GPRO {
    /**
     * \ingroup gpro
     * \class Application
     * \brief To initialize or finalize outside frameworks such as MPI 
     */
    class Application {
    public:
        /**
         * \brief initialize outside framework
         * \param[in] programType type of outside framework
         * \param[in] argc same as the main function
         * \param[in] argv same as the main function
         */
        static bool START( ProgramType programType, int argc, char *argv[] );
         /**
         * \brief finalize outside framework
         */
        static bool END();

    public:
        static ProgramType _programType; //serial, MPI, openMP or CUDA program
    };
};

#endif