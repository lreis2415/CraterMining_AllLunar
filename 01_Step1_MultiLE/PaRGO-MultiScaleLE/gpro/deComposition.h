#ifndef DeComposition_H
#define DeComposition_H

#include "basicTypes.h"
#include "cellSpace.h"
#include "neighborhood.h"
#include "metaData.h"

#define Eps 0.0000001

namespace GPRO {
    template<class elemType>
    class ComputeLayer;

	/**
     * \ingroup gpro
     * \class DeComposition 
     * \brief Decompose a layer to smaller parcels
     */
    template<class elemType>
    class DeComposition {
    public:
        DeComposition()
            : _pNbrhood( 0 ) {}

        DeComposition( const SpaceDims &cellSpaceDims, const Neighborhood <elemType> &nbrhood );

        ~DeComposition() {}

        bool rowDcmp( MetaData &metaData, int nSubSpcs ) const;
        bool colDcmp( MetaData &metaData, int nSubSpcs ) const;
        /*bool blockDcmp(MetaData &metaData,
                       int nRowSubSpcs,
                       int nColSubSpcs) const;*/
		//TODO: extend to _val1DDcmp
        bool valRowDcmp( vector<CoordBR> &vDcmpIdx, ComputeLayer<elemType> &computLayer, int nSubSpcs ) const;

    private:
        /**
         * \brief simple linear decomposition
         *  
         * divide the range between glbBegin and glbEnd, equally to nSubSpcs parcels
         * \param[out] subBegin the begin index of this decomposition
         * \param[out] subEnd the end index of this decomposition
         * \param[in] glbBegin begin index of the global work bounding rectangle
         * \param[in] glbEnd end index of the global work bounding rectangle
         * \param[in] nSubSpcs num of result parcels
         * \param[in] iSubSpc index of this parcel among the result parcels
         */
        void _smpl1DDcmp( int &subBegin, int &subEnd,
                          int glbBegin, int glbEnd,
                          int nSubSpcs, int iSubSpc ) const;

    private:
        SpaceDims _glbDims;
        CoordBR _glbWorkBR; ///< ACTUAL BR. (refer to metaData.h)
        const Neighborhood <elemType> *_pNbrhood;
    };
};

/****************************************
*             Private Methods           *
*****************************************/


template<class elemType>
void GPRO::DeComposition<elemType>::
_smpl1DDcmp( int &subBegin, int &subEnd,
             int glbBegin, int glbEnd,
             int nSubSpcs, int iSubSpc ) const {
    int glbRange = glbEnd - glbBegin + 1;
    int remainder = glbRange % nSubSpcs;
    int blockSize;
    if ( remainder == 0 ) {
        blockSize = glbRange / nSubSpcs;
        subBegin = glbBegin + iSubSpc * blockSize;
        subEnd = subBegin + blockSize - 1;
    } else {
        blockSize = glbRange / nSubSpcs + 1;
        if ( iSubSpc < remainder ) {
            subBegin = glbBegin + iSubSpc * blockSize;
            subEnd = subBegin + blockSize - 1;
        } else {
            if ( iSubSpc == remainder ) {
                subBegin = glbBegin + iSubSpc * blockSize;
                subEnd = subBegin + blockSize - 2;
            } else {
                subBegin = glbBegin
                    + remainder * blockSize
                    + ( iSubSpc - remainder ) * ( blockSize - 1 );
                subEnd = subBegin + blockSize - 2;
            }
        }
    }
}

/****************************************
*             Public Methods            *
*****************************************/

/**
 * \brief simple linear decomposition
 * \param[out] subBegin the begin index of this decomposition
 * \param[out] subEnd the end index of this decomposition
 * \param[in] glbBegin begin index of the global work bounding rectangle
 * \param[in] glbEnd end index of the global work bounding rectangle
 * \param[in] nSubSpcs num of  ( processors, threads etc.)
 * \param[in] iSubSpc rank
 */
template<class elemType>
GPRO::DeComposition<elemType>::
DeComposition( const SpaceDims &cellSpaceDims, const Neighborhood <elemType> &nbrhood ) {
    if ( !nbrhood.calcWorkBR( _glbWorkBR, cellSpaceDims )) {
        cerr << __FILE__ << " " << __FUNCTION__ \
			 << " Error: invalid Neighborhood to construct a DeComposition" \
			 << endl;
        exit( 1 );
    }
    _glbDims = cellSpaceDims;
    _pNbrhood = &nbrhood;
}

/**
 * \brief row-wise decomposition
 * \param[out] metaData 
 * \param[in] nSubSpcs
 */
template<class elemType>
bool GPRO::DeComposition<elemType>::
rowDcmp( MetaData &metaData, int nSubSpcs ) const {
    if ( nSubSpcs < 1 || nSubSpcs > _glbWorkBR.nRows()) {
        cerr << __FILE__ << " " << __FUNCTION__ \
             << " Error: invalid number of SubSpaces (" << nSubSpcs << ")" \
             << " considering the global working bounding rectangle (" << _glbWorkBR << ")" \
             << endl;
        return false;
    }

    //DomDcmpType dcmpType = ROWWISE_DCMP;
    //metaData._domDcmpType = dcmpType;

    int glbBegin = _glbWorkBR.nwCorner().iRow();
    int glbEnd = _glbWorkBR.seCorner().iRow();
    int iSubSpc = metaData.myrank;
    int subBegin, subEnd;
    _smpl1DDcmp( subBegin, subEnd,
                 glbBegin, glbEnd,
                 nSubSpcs, iSubSpc );

    CellCoord nwCorner( subBegin + _pNbrhood->minIRow(), 0 );
    CellCoord seCorner( subEnd + _pNbrhood->maxIRow(), _glbDims.nCols() - 1 );
    CoordBR subMBR( nwCorner, seCorner );
    metaData._MBR = subMBR;

    SpaceDims dims( subMBR.nRows(), subMBR.nCols() );
    metaData._localdims = dims;
    CoordBR workBR;
    if ( !_pNbrhood->calcWorkBR( workBR, dims )) {
        return false;
    }
	metaData._localworkBR = workBR;
    return true;
}

/**
 * \brief col-wise decomposition
 * \param[out] metaData 
 * \param[in] nSubSpcs
 */
template<class elemType>
bool GPRO::DeComposition<elemType>::
colDcmp( MetaData &metaData, int nSubSpcs ) const {
    if ( nSubSpcs < 1 || nSubSpcs > _glbWorkBR.nCols()) {
        cerr << __FILE__ << " " << __FUNCTION__ \
			 << " Error: invalid number of SubSpaces (" << nSubSpcs << ")" \
			 << " considering the global working bounding rectangle (" << _glbWorkBR << ")" \
			 << endl;
        return false;
    }

    int glbBegin = _glbWorkBR.nwCorner().iCol();
    int glbEnd = _glbWorkBR.seCorner().iCol();
    int iSubSpc = metaData.myrank;
    int subBegin, subEnd;
    _smpl1DDcmp( subBegin, subEnd,
                 glbBegin, glbEnd,
                 nSubSpcs, iSubSpc );

	CellCoord nwCorner( 0, subBegin + _pNbrhood->minICol());
    CellCoord seCorner( _glbDims.nRows() - 1, subEnd + _pNbrhood->maxICol());
    CoordBR subMBR( nwCorner, seCorner );
    metaData._MBR = subMBR;

    SpaceDims dims( subMBR.nRows(), subMBR.nCols());
    metaData._localdims = dims;
    CoordBR workBR;
    if ( !_pNbrhood->calcWorkBR( workBR, dims )) {
        return false;
    }
    metaData._localworkBR = workBR;
	//cout<<workBR.minIRow()<<" "<<workBR.minICol()<<" "<<workBR.maxIRow()<<" "<<workBR.maxICol()<<endl;

    return true;
}

/**
 * \brief 
 * \param[out]
 * \param[in] 
 */
template<class elemType>
bool GPRO::DeComposition<elemType>::
valRowDcmp( vector<CoordBR> &vDcmpBR, ComputeLayer<elemType> &layer, int nSubSpcs ) const {
    int myRank, process_nums;
    MPI_Comm_rank(MPI_COMM_WORLD, &myRank);
    MPI_Comm_size(MPI_COMM_WORLD, &process_nums);
    //only accessed by the main process, divide the whole layer.
    //bound dividing should be updated if parallized.
    if ( nSubSpcs < 1 || nSubSpcs > _glbWorkBR.nRows()) {
        cerr << __FILE__ << " " << __FUNCTION__ \
			 << " Error: invalid number of SubSpaces (" << nSubSpcs << ")" \
			 << " considering the global working bounding rectangle (" << _glbWorkBR << ")" \
			 << endl;
        return false;
    }

    CellSpace<elemType> &comptL = *( layer.cellSpace());
    double *rowComptLoad = new double[layer._pMetaData->_glbDims.nRows()];
    double totalComptLoad = 0.0;

    for ( int cRow = 0; cRow < layer._pMetaData->_glbDims.nRows(); cRow++ ) {
        rowComptLoad[cRow] = 0.0;
        for ( int cCol = 0; cCol < layer._pMetaData->_glbDims.nCols(); cCol++ ) {
			//why judge -9999 specifically
            if (( comptL[cRow][cCol] + 9999 ) > Eps && ( comptL[cRow][cCol] - layer._pMetaData->noData ) > Eps ) {
                rowComptLoad[cRow] += comptL[cRow][cCol];
            }
        }
        totalComptLoad += rowComptLoad[cRow];

    }

    double averComptLoad = totalComptLoad / ( nSubSpcs );
    cout<<"rank "<<myRank<<". avg compt load: "<<averComptLoad<<endl;
    double accuComptLoad = 0;
    int subBegin = 0;
    int subEnd = subBegin;    //at least assign 1 row in the spatial computational domain
    for ( int i = 0; i < nSubSpcs - 1; ++i ) {    //find nSubSpcs-1 positions
        double subComptLoad = 0.0;
        double minComptDiff = 0.0;
        //for ( int cRow = subBegin; cRow <= layer._pMetaData->_MBR.maxIRow(); cRow++ ) {
        for ( int cRow = subBegin; cRow < _glbDims.nRows(); cRow++ ) {
            int rowGap = cRow - 0;
            subComptLoad += rowComptLoad[rowGap];
            accuComptLoad += rowComptLoad[rowGap];
            if ( subComptLoad <= averComptLoad && _glbDims.nRows()-1-cRow>nSubSpcs-1-i) {
                if ( fabs( minComptDiff ) < Eps || ( averComptLoad - subComptLoad ) < minComptDiff ) {
                    minComptDiff = averComptLoad - subComptLoad;
                }
            } else {
                if ( fabs( minComptDiff ) < Eps || ( subComptLoad - averComptLoad ) <= minComptDiff || _glbDims.nRows()-1-cRow==nSubSpcs-1-i) {
                    subEnd = cRow;
                    CellCoord nwCorner( subBegin, 0 );
                    CellCoord seCorner( subEnd, layer._pMetaData->_MBR.maxICol());
                    CoordBR subMBR( nwCorner, seCorner );
                    vDcmpBR.push_back( subMBR );
                    averComptLoad = ( totalComptLoad - accuComptLoad ) / ( nSubSpcs - i - 1 );
                    subBegin = cRow + 1;
                } else {
                    subEnd = cRow - 1;
                    accuComptLoad -= rowComptLoad[rowGap];
                    CellCoord nwCorner( subBegin, 0 );
                    CellCoord seCorner( subEnd, layer._pMetaData->_MBR.maxICol());
                    CoordBR subMBR( nwCorner, seCorner );
                    vDcmpBR.push_back( subMBR );
                    subComptLoad -= rowComptLoad[rowGap];
                    averComptLoad = ( totalComptLoad - accuComptLoad ) / ( nSubSpcs - i - 1 );
                    subBegin = cRow;
                }
                break;
            }
        }
    }
    //from subBegin to the end
    CellCoord nwCorner( subBegin, 0 );
    CellCoord seCorner( layer._pMetaData->_MBR.maxIRow(), layer._pMetaData->_MBR.maxICol());
    CoordBR subMBR( nwCorner, seCorner );
    vDcmpBR.push_back( subMBR );
    delete[]rowComptLoad;
    return true;
}

#endif
