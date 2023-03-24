package com.example.drugidentification;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.app.Activity;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class scanText extends AppCompatActivity {

    Button select;
    Bitmap bitmap;
    ImageView img;
    Uri selectedImage;
    Uri image_uri;
    final int PERMISSION_CODE = 1000;
    String rootURL = "https://bd2e-174-93-236-22.ngrok.io";
    String func ="uploadPill";
    String url = rootURL + "/" + func;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_text);

        select = findViewById(R.id.selectTxt);
        img = findViewById(R.id.imageTxt);


        selectedImage = getIntent().getParcelableExtra("image_uri");

        if (selectedImage != null) {

            Intent cropper = new Intent(getApplicationContext(), cropperActivity.class);
            cropper.putExtra("data", selectedImage.toString());
            startActivityForResult(cropper, 101);
            setImage(selectedImage);
        }
    }

    public void select(View v) {
        Intent intent = new Intent(Intent.ACTION_PICK);
        intent.setType("image/*");

        String[] mimeTypes = {"image/jpg", "image/png"};
        intent.putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes);

        getContent.launch(intent);

    }

    ActivityResultLauncher<Intent> getContent = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent data = result.getData();
                        selectedImage = data.getData();


                        Intent cropper = new Intent(getApplicationContext(), cropperActivity.class);
                        cropper.putExtra("data", selectedImage.toString());
                        startActivityForResult(cropper, 101);

                    }
                }
            });

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(resultCode==-1 && requestCode==101){
            String result = data.getStringExtra("result");
            Uri resultUri = null;
            if(result!=null){
                resultUri = Uri.parse(result);
            }

            setImage(resultUri);
        }

    }

    public void getResults(View v){
        try {
            bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), selectedImage);
        } catch (IOException e) {
            e.printStackTrace();
        }

        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
//        Bitmap resized = Bitmap.createScaledBitmap(bitmap, 224, 224, true);

        if(bitmap != null){

            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
            byte[] bytes = byteArrayOutputStream.toByteArray();

            final String base64img = Base64.encodeToString(bytes, Base64.DEFAULT);

            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            JSONObject object;
                            System.out.println(response);
                            try {
                                object = new JSONObject(response);
                                String sum_text = object.getString("sum_texts");
                                String prob = object.getString("urls");

                                if(sum_text.equals("")){
                                    Toast.makeText(getApplicationContext(), "Sorry, can't retrieve information.", Toast.LENGTH_SHORT).show();
                                }else{
                                    Intent i = new Intent(getApplicationContext(), showSummary.class);
                                    Bundle b = new Bundle();
                                    b.putString("summary", sum_text);
                                    i.putExtras(b);
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
                    paramV.put("data", base64img);
                    System.out.println("sending request");
                    return paramV;
                }
            };
            queue.add(stringRequest);

        }
        else{
            Toast.makeText(getApplicationContext(), "Upload a picture", Toast.LENGTH_SHORT).show();
        }
    }

    public void captureImage (View v){

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(android.Manifest.permission.CAMERA) ==
                    PackageManager.PERMISSION_DENIED ||
                    checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE) ==
                            PackageManager.PERMISSION_DENIED) {
                String[] permission = {android.Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE};
                requestPermissions(permission, PERMISSION_CODE);


            } else {
                openCamera();
            }
        } else {
            openCamera();
        }
    }

    public void openCamera () {


        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "New Picture");
        values.put(MediaStore.Images.Media.DESCRIPTION, "From the Camera");

        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);

        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        someActivityResultLauncher.launch(cameraIntent);
    }

    ActivityResultLauncher<Intent> someActivityResultLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {


                        Intent i = new Intent(getApplicationContext(), MainActivity.class);


                        i.putExtra("image_uri", image_uri);
                        startActivity(i);

                    }
                }
            });

    @Override
    public void onRequestPermissionsResult ( int requestCode, @NonNull String[] permissions,
                                             @NonNull int[] grantResults){
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        switch (requestCode) {
            case PERMISSION_CODE: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    openCamera();
                } else {
                    Toast.makeText(this, "Permission denied ...", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }


    public void setImage (Uri image_uri){
        img.setImageURI(image_uri);
    }
}