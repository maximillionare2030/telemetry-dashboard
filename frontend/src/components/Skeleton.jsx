import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

const SkeletonComponent = () => {
    return (
        <div className="container skeleton">
            <Skeleton 
                count={5}   
                height={100} 
                width="100%"
                baseColor="#232325"
                highlightColor="#3C3C3C"
                duration={1.5}
                style={{
                    marginBottom: '4px',
                    borderRadius: '4px'
                }}
                containerClassName="skeleton-elements"
            />
        </div>
    )
}

export default SkeletonComponent