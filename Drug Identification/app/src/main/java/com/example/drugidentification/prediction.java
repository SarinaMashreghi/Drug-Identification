package com.example.drugidentification;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class prediction extends AppCompatActivity {

    String rootURL = "https://797e-174-93-236-22.ngrok.io ";
    String func ="getInfo";
    String url = rootURL + "/" + func;
    String prediction;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prediction);

        TextView predTxt = findViewById(R.id.pred_txt);
        TextView accTxt = findViewById(R.id.acc_txt);

        Button infoBtn = findViewById(R.id.info_btn);
        Button Home = findViewById(R.id.homeBtn);


        Intent i = getIntent();
        Bundle b = i.getExtras();

        prediction = b.getString("class");
        String prob = b.getString("prob");
//        infoBtn.setOnClickListener(getInfo());


//        predTxt.setText("Predicted Letter: W");
//        accTxt.setText("Accuracy: 92%");
        predTxt.setText(prediction);
        accTxt.setText("Accuracy: "+ prob);
    }

    public void goHome(View v){
        Intent i = new Intent(getApplicationContext(), MainActivity.class);
        startActivity(i);

    }
    public void getInfo(View v){

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        JSONObject object;
                        System.out.println(response);
                        try {
                            object = new JSONObject(response);
                            String info = object.getString("info");
                            System.out.println(info);

//                            if(class_name.equals("0")){
//                                Toast.makeText(getApplicationContext(), "Sorry, can't identify the packaging, try again.", Toast.LENGTH_SHORT).show();
//                            }else{
//                                Intent i = new Intent(getApplicationContext(), prediction.class);
//                                Bundle b = new Bundle();
//                                b.putString("class", "The medication is "+class_name);
//                                b.putString("prob", prob);
//                                i.putExtras(b);
//                                startActivity(i);
//                            }

                            if(info!=null){
                                Intent i = new Intent(getApplicationContext(), prediction.class);
                                Bundle b = new Bundle();
                                b.putString("info", "Information about "+prediction+":\n"+info);
                                i.putExtras(b);
                                startActivity(i);}
                            else{
                                Intent i = new Intent(getApplicationContext(), error.class);

                                startActivity(i);
                            }


                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

//                            if(response.equals("success")){
//                                Toast.makeText(getApplicationContext(), "Upload successful", Toast.LENGTH_SHORT).show();
//                            } else Toast.makeText(getApplicationContext(), "Upload failed", Toast.LENGTH_SHORT).show();
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(), "error", Toast.LENGTH_LONG).show();
            }
        }){
            protected Map<String, String> getParams(){
                Map<String, String> paramV = new HashMap<>();
                paramV.put("name", prediction);
                System.out.println("sending request");
                return paramV;
            }
        };
        queue.add(stringRequest);
    }
}