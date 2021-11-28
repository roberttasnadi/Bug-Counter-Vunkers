package com.atra.bahar.bugsdetector

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.fragment.app.Fragment
import com.atra.bahar.bugsdetector.Controllers.HomeFragment
import com.google.android.material.bottomnavigation.BottomNavigationView

class MainActivity : AppCompatActivity() {
    // Anar al enviorment i executar activate, después flask run --host = 0.0.0.0
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Crear las opciones del menu de navegación y asignarles un fragmento.
        var navigationView = findViewById<BottomNavigationView>(R.id.navigationView)
        navigationView.setOnNavigationItemSelectedListener { menuItem ->
            when (menuItem.itemId) {
                R.id.action_home -> {
                    val fragment = HomeFragment()
                    openFragment(fragment)
                    true
                }
                else -> false
            }
        }

        navigationView.selectedItemId = R.id.action_home

    }

    private fun openFragment(fragment: Fragment) {
        """
            Changes the actual fragment displayed in function
             of the selected option from the navegation menu.
        """.trimIndent()
        val transaction = supportFragmentManager.beginTransaction()
        transaction.replace(R.id.mainContainer, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

}