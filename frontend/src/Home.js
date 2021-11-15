import React,{useState} from 'react'
import './css/home.scss'
import { FaLeaf } from "react-icons/fa";
import BeforeAfter from './BeforeAfter'
import axios from 'axios'

export default function Home() {
   
    const [compressRate,setCompressRate] = useState(50)
    const [uploadedImage,setUploadedImage]= useState(null)
    const [newImageData,setNewImageData] = useState({
        img_url:'',
        size_before:'',
        size_after:'',
        resolution_before:'',
        resolution:''
    })
   const [resolution,setResolution] = useState({
    x_resolution:1,
    y_resolution:1
   })
    const {x_resolution,y_resolution} = resolution

    const onRangeChange=(e)=>{
          
          setCompressRate(e.target.value)
    }


   const onFileChange=async(e)=>{
       
       setUploadedImage(e.target.files[0])
       try{
           await axios.delete(`${process.env.REACT_APP_API_URL}/delete_old_media/`)
       }catch(err){
           
       }
   }
   const onResolutionChange=(e)=>{
       setResolution({
           ...resolution,[e.target.name]:e.target.value
       })
   }

   const onCompressClick=async(action)=>{
       window.scrollTo({
           top:400,
           behavior:'smooth'
       })
    
       const config ={
           headers:{
               'content-type':'multipart/form-data',
               'accept':'application/json',
           }
       }
         
       try{
            const form_data = new FormData()
            form_data.append('uploaded_image',uploadedImage)
            if(action === 'compress'){
                form_data.append('compress_percentage',compressRate)
                form_data.append('action','compress')
            }else{
                form_data.append('resize_measure_x',x_resolution)
                form_data.append('resize_measure_y',y_resolution)
                form_data.append('action','resize')
            }
            

            const res =await axios.post(`${process.env.REACT_APP_API_URL}/upload/post_image/`,form_data,config )
            const data =await res.data

            if(data.img_id){
                const new_res = await axios({
                    method:'GET',
                    Accept:'application/json',
                    
                 url:`${process.env.REACT_APP_API_URL}/upload/post_image/${data.img_id}`,
                 
                })
                const new_data = await new_res.data
                   
                setNewImageData({
                    img_url:new_data.uploaded_image,
                    size_before:new_data.current_size,
                    size_after:new_data.size_after,
                    resolution_before:new_data.orignal_size_x_y,
                    resolution:`${ new_data.resize_measure_x } * ${new_data.resize_measure_y}` 
                })
                console.log(new_data);
            }
            console.log(data);
       }catch(err){
           console.log(err);
       }
   }



    return (
        <>
          <section>
              <nav>
                  <div className="logo"><FaLeaf /> <h1>VISH</h1></div>
                  <div className="work"><h3>Image Compress/Resize</h3></div>
              </nav>
              <div className="container">
                  <div className="form_container">
                      <form action="">
                          <div className="input-field">
                          <label htmlFor="upload_image">Upload Image</label><br />
                          <input onChange={onFileChange} type="file" name="file" id="upload_image" />
                          
                          </div>
                      </form>
                      <div className="action">
                          <div className="compress-div">
                              {uploadedImage ? (
                                <button onClick={()=>onCompressClick('compress')} className='compress-btn'>Compress</button>
                              ):(<button onClick={()=>onCompressClick('compress')} disabled className='compress-btn disabled'>Compress</button>)}
                              
                              <div className="compress-range">
                              <p>{compressRate}</p>
                              <input  value={compressRate}  onChange={onRangeChange} type="range" name="" id=""  min="1" max="100" />
                              </div>
                             
                          </div>
                          <div className="resize-div">
                              {x_resolution > 0 && y_resolution > 0 && uploadedImage ? (
                                <button onClick={()=>onCompressClick('resize')}  className='resize-btn'>Resize</button>
                              ):(<button onClick={()=>onCompressClick('resize')} disabled className='resize-btn disabled'>Resize</button>)}
                          
                          <div className="resize-range">
                              <input placeholder='X' value={x_resolution} onChange={onResolutionChange} type="number" name="x_resolution" />
                              <input placeholder='Y' value={y_resolution} onChange={onResolutionChange} type="number" name="y_resolution"  />
                          </div>
                          </div>
                      </div>
                  </div>
              </div>
              <BeforeAfter uploadedImage={uploadedImage} setNewImageData={setNewImageData} newImageData={newImageData} />
          </section>
        </>
    )
}
