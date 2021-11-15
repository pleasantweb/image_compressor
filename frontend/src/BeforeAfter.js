import React,{useState,useEffect} from 'react'

export default function BeforeAfter(props) {
   const [image,setImage]=useState("")
       const {uploadedImage,setNewImageData,newImageData} = props
   useEffect(()=>{
       
       if(uploadedImage){
           setNewImageData({
            img_url:"",
            size_before:'',
            size_after:'',
            resolution_before:"",
            resolution:''
           })
          
        let src=URL.createObjectURL(uploadedImage)
           setImage(src)
        
       }
   },[uploadedImage,setNewImageData])

    return (
        <div className="before-after">
            <div className="before">
                {image !== "" ?(
                    <>
                 <h1>BEFORE</h1>
                <img src={image} alt="" />
                <div className="size-resolution">
                <div className="size">{newImageData.size_before}</div>
                <div className="resolution">{newImageData.resolution_before}</div>
                </div>
                    </>
                ):(<div></div>)}
                
               
                
            </div>
            <div className="after">
                {newImageData.img_url !== "" ? (
                  <>
                <h1>AFTER</h1>
                <div className="img-div">
                <img src={newImageData.img_url} alt="" />
                <div className="img-hover">
                    <a href={newImageData.img_url} download>Click to Download</a>
                </div>
                </div>
                <div className="size-resolution">
                <div className="size">{newImageData.size_after}</div>
                <div className="resolution">{newImageData.resolution}</div>
                </div>
</>
                ):(<div></div>)}
                
                
            </div>
        </div>

    )
}
