package com.ykbintang.envy.views.soil

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import androidx.activity.viewModels
import com.google.android.material.snackbar.Snackbar
import com.ykbintang.envy.R
import com.ykbintang.envy.databinding.ActivitySoilBinding
import com.ykbintang.envy.models.PredictSoilRequest
import com.ykbintang.envy.viewModels.SoilViewModel

class SoilActivity : AppCompatActivity() {
    private lateinit var binding: ActivitySoilBinding
    private val viewModel by viewModels<SoilViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivitySoilBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.materialToolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.deteksi_tanah)

        binding.btnDetect.setOnClickListener { detect() }
        viewModel.result.observe(this) {
            if (it.isNotEmpty()) {
                binding.llResult.visibility = View.VISIBLE
                binding.tvResult.text = getString(
                    R.string.sistem_kami_memprediksi_bahwa_kualitas_tanah_di_tempat_kamu,
                    it
                )
            }
        }
        viewModel.onError.observe(this) {
            if (it.isNotEmpty()) Snackbar.make(binding.root, it, Snackbar.LENGTH_SHORT).show()
        }
        viewModel.isLoading.observe(this) {
            binding.btnDetect.isEnabled = !it
        }
    }

    private fun detect() {
        val n = binding.etNitrogen.text.toString()
        val p = binding.etPhosporus.text.toString()
        val potassium = binding.etPotassium.text.toString()
        val ph = binding.etPh.text.toString()

        if (n.isEmpty() || p.isEmpty() || ph.isEmpty() || potassium.isEmpty())
            Snackbar.make(binding.root, "Silahkan isi semua field!", Snackbar.LENGTH_SHORT).show()
        else {
            val predictSoilRequest = PredictSoilRequest(n.toInt(), p.toInt(), potassium.toInt(), ph.toInt())
            viewModel.detect(predictSoilRequest)
        }
    }
}