package com.ykbintang.envy.views.water

import android.os.Bundle
import android.view.View
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.snackbar.Snackbar
import com.ykbintang.envy.R
import com.ykbintang.envy.databinding.ActivityWaterBinding
import com.ykbintang.envy.models.PredictWaterRequest
import com.ykbintang.envy.viewModels.WaterViewModel

class WaterActivity : AppCompatActivity() {
    private lateinit var binding: ActivityWaterBinding
    private val viewModel by viewModels<WaterViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityWaterBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.materialToolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.deteksi_air)

        binding.btnDetect.setOnClickListener { detect() }
        viewModel.result.observe(this) {
            if (it.isNotEmpty()) {
                binding.llResult.visibility = View.VISIBLE
                binding.tvResult.text = getString(
                    R.string.sistem_kami_memprediksi_bahwa_kualitas_air_di_tempat_kamu,
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
        val fc = binding.etFc.text.toString()
        val o2 = binding.etO2.text.toString()
        val ph = binding.etPh.text.toString()
        val tss = binding.etTss.text.toString()
        val temp = binding.etTemp.text.toString()
        val n = binding.etNitrogen.text.toString()
        val p = binding.etPhosporus.text.toString()
        val turb = binding.etTurbidity.text.toString()

        if (fc.isEmpty() || o2.isEmpty() || ph.isEmpty() || tss.isEmpty() || temp.isEmpty() || n.isEmpty() || p.isEmpty() || turb.isEmpty())
            Snackbar.make(binding.root, "Silahkan isi semua field!", Snackbar.LENGTH_SHORT).show()
        else {
            val predictWaterRequest = PredictWaterRequest(
                fc.toInt(),
                o2.toInt(),
                ph.toInt(),
                tss.toInt(),
                temp.toInt(),
                n.toInt(),
                p.toInt(),
                turb.toInt()
            )
            viewModel.detect(predictWaterRequest)
        }
    }
}