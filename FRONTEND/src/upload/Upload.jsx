import React, { useState } from 'react'


const Upload = () => {
    const [files,setFiles]=useState(null)
    const [message,setMessage]=useState('')
    const [numberOfFiles,setNumberOfFiles]=useState(0)

    const handleUpload=async (e)=>{
        e.preventDefault()
        if (!files || files.length === 0) {
            setMessage("Please select files first.")
            return
        }
        const formData=new FormData()
        for(let i=0;i<files.length;i++){
            formData.append("files",files[i])
        }
        try{
            const response=await fetch("https://rag-zmjw.onrender.com/uploadFiles",{
                method:"POST",
                body:formData
            })
            const data= await response.json()
            localStorage.setItem("file_id", data.file_id)
            console.log(data.file_id)
            if(response.ok){
                setMessage(data.status)
                setNumberOfFiles(data.numberOfFiles)
            }else{
                setMessage("upload failed")
                setNumberOfFiles(0)
            }


        }catch (e){
            setMessage("Error While uploading file.")
        }
    }
  return (
    <div>
      <div>
        <form onSubmit={handleUpload}>
            <input type="file" multiple onChange={(e)=>setFiles(e.target.files)}/>
            <button type='submit'>upload</button>
            <p>{message}</p>
            <p>{numberOfFiles}</p>
        </form>
      </div>
    </div>
  )
}

export default Upload