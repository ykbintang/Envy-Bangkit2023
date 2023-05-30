package com.ykbintang.envy.views.home

import android.content.Intent
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.ykbintang.envy.R
import com.ykbintang.envy.databinding.FragmentHomeBinding
import com.ykbintang.envy.views.air.AirActivity
import com.ykbintang.envy.views.soil.SoilActivity
import com.ykbintang.envy.views.water.WaterActivity

class HomeFragment : Fragment() {
    private lateinit var binding: FragmentHomeBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentHomeBinding.inflate(layoutInflater)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.apply {
            btnDetectWater.setOnClickListener {
                Intent(requireContext(), WaterActivity::class.java).also {
                    startActivity(it)
                }
            }
            btnDetectEarth.setOnClickListener {
                Intent(requireContext(), SoilActivity::class.java).also {
                    startActivity(it)
                }
            }
            btnDetectAir.setOnClickListener {
                Intent(requireContext(), AirActivity::class.java).also {
                    startActivity(it)
                }
            }
        }
    }
}