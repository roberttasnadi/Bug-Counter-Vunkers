package com.atra.bahar.bugsdetector.Controllers

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.atra.bahar.bugsdetector.databinding.FragmentHomeBinding
import java.io.File
import com.android.volley.Request
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.atra.bahar.bugsdetector.Model.BugsDetectorDTO
import com.google.gson.Gson


class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    val REQUEST_CODE = 100


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)

        binding.uploadButton.setOnClickListener {
            openGalleryForImage()
        }

        return binding.root
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == Activity.RESULT_OK && requestCode == REQUEST_CODE){
            val f = File(data?.dataString!!)
            val imageName: String = f.getName()
            val filename: String = imageName.substring(imageName.lastIndexOf("F") + 1)
            binding.bugsImage.setImageURI(data.data)
            processImage(filename)
        }
    }


    fun processImage(path: String){
        """
            Sends to the api the desired image to process and waits for a response.
        """.trimIndent()
        val queue = Volley.newRequestQueue(requireContext())
        val url = "http://172.20.10.3:5000/processImage?path=$path"
        val gson = Gson()
        val stringRequest = StringRequest(Request.Method.GET, url,
            { response ->
                var data = gson.fromJson(response.toString(), BugsDetectorDTO::class.java)
                binding.tinyTV.text = "Mosquitos pequeños: ${data.tinyMosquito}"
                binding.flyTV.text = "Moscas: ${data.fly}"
                binding.bigTV.text = "Mosquitos grandes: ${data.bigMosquito}"
                binding.normalTV.text = "Mosquitos: ${data.normalMosquito}"
            },
            { error ->
                Log.e("ERROR", error.message.toString())
            })
        queue.add(stringRequest)
    }

    // Abre la galeria para seleccionar imagen
    private fun openGalleryForImage() {
        """
            function that starts an intent to open the gallery to select an image
        """.trimIndent()
        val intent = Intent(Intent.ACTION_PICK)
        intent.type = "image/*"
        startActivityForResult(intent, REQUEST_CODE)
    }

}


