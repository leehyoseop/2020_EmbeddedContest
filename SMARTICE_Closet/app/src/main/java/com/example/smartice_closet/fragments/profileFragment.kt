package com.example.smartice_closet.fragments

import android.os.Bundle
import android.text.Editable
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.example.smartice_closet.R
import com.example.smartice_closet.profileGET.profileGETRequest
import com.example.smartice_closet.profileGET.profileGETResponse
import com.example.smartice_closet.profilePOST.profilePOSTRequest
import com.example.smartice_closet.profilePOST.profilePOSTResponse
import kotlinx.android.synthetic.main.fragment_profile.*
import retrofit2.*
import retrofit2.converter.gson.GsonConverterFactory

/**
 * A simple [Fragment] subclass.
 * Use the [profileFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class profileFragment : Fragment() {

    private val USERNAME = "USERNAME"
    private val TOKEN = "USERTOKEN"

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_profile, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val bundle = arguments
        val userName = bundle!!.getString(USERNAME)
        val userToken = bundle!!.getString(TOKEN)
        Log.d("onViewCreated", userName + userToken)
        
        getFromServer(userToken)

        setUserName(userName)

        update_btn.setOnClickListener {
            sendToServer(userToken)

        }
    }

    private fun setUserName(userName: String?) {
        user_Name.text = "${userName}".toUpperCase()
        small_user_Name.text = "${userName}".toLowerCase()
        profile_Name_eT.text = Editable.Factory.getInstance().newEditable(userName)
    }

    private fun getFromServer(userToken: String?) {
        val BaseURL = "http://ec2-13-124-208-47.ap-northeast-2.compute.amazonaws.com:8000"

        val retrofit = Retrofit.Builder()
            .baseUrl(BaseURL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val profileGETService = retrofit.create(profileGETRequest::class.java)
        val call = userToken?.let { profileGETService.getUserInfo(token = it) }

        if (call != null) {
            call.enqueue(object : Callback<profileGETResponse> {
                override fun onFailure(call: Call<profileGETResponse>, t: Throwable) {
                    Log.d("onFailure(ProfileGET)", "message : " + t.message)
                }

                override fun onResponse(call: Call<profileGETResponse>, response: Response<profileGETResponse>) {
                    if (response.code() == 200) {
                        val profileResponse = response.body()
                        Log.d("onResponse(Weather)", "messsage : " + profileResponse?.code)
                        Log.d("onResponse(Weather)", "messsage : " + profileResponse?.email)
                        Log.d("onResponse(Weather)", "messsage : " + profileResponse?.raspIp)
                        Log.d("onResponse(Weather)", "messsage : " + profileResponse?.raspPort)

                        var email = profileResponse?.email
                        var raspIp = profileResponse?.raspIp
                        var raspPort = profileResponse?.raspPort

                        profile_Email_eT.text = Editable.Factory.getInstance().newEditable(email)
                        profile_IP_eT.text = Editable.Factory.getInstance().newEditable(raspIp)
                        profile_PORT_eT.text = Editable.Factory.getInstance().newEditable(raspPort)

                    }
                }
            })
        }
    }

    private fun sendToServer(userToken: String?) {
        val BaseURL = "http://ec2-13-124-208-47.ap-northeast-2.compute.amazonaws.com:8000"
        var userIP = profile_IP_eT.text.toString()
        var userPORT = profile_PORT_eT.text.toString()

        val retrofit = Retrofit.Builder()
            .baseUrl(BaseURL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val profilePOSTService = retrofit.create(profilePOSTRequest::class.java)
        val call = userToken?.let { profilePOSTService.sendUserInfo(token = it, raspIp = userIP, raspPORT = userPORT) }

        if (call != null) {
            call.enqueue(object : Callback<profilePOSTResponse> {
                override fun onFailure(call: Call<profilePOSTResponse>, t: Throwable) {
                    Log.d("onFailure(ProfilePOST)", "message : " + t.message)
                }

                override fun onResponse(call: Call<profilePOSTResponse>, response: Response<profilePOSTResponse>) {
                    if (response.code() == 201) {
                        Toast.makeText(context, "정보가 업데이트 되었습니다.", Toast.LENGTH_SHORT).show()
                    }
                    else {
                        Log.d("onResponse", "ERROR")
                    }
                }

            })
        }
    }






}