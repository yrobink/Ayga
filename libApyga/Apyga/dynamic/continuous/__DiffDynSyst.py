# -*- coding: utf-8 -*-

##################################################################################
##################################################################################
##                                                                              ##
## Copyright Yoann Robin, 2018                                                  ##
##                                                                              ##
## yoann.robin.k@gmail.com                                                      ##
##                                                                              ##
## This software is a computer program that is part of the Apyga library. This  ##
## library makes it possible to study dynamic systems and to statistically      ##
## correct uni / multivariate data by applying optimal transport to             ##
## sparse histograms.                                                           ##
##                                                                              ##
## This software is governed by the CeCILL-C license under French law and       ##
## abiding by the rules of distribution of free software.  You can  use,        ##
## modify and/ or redistribute the software under the terms of the CeCILL-C     ##
## license as circulated by CEA, CNRS and INRIA at the following URL            ##
## "http://www.cecill.info".                                                    ##
##                                                                              ##
## As a counterpart to the access to the source code and  rights to copy,       ##
## modify and redistribute granted by the license, users are provided only      ##
## with a limited warranty  and the software's author,  the holder of the       ##
## economic rights,  and the successive licensors  have only  limited           ##
## liability.                                                                   ##
##                                                                              ##
## In this respect, the user's attention is drawn to the risks associated       ##
## with loading,  using,  modifying and/or developing or reproducing the        ##
## software by the user in light of its specific status of free software,       ##
## that may mean  that it is complicated to manipulate,  and  that  also        ##
## therefore means  that it is reserved for developers  and  experienced        ##
## professionals having in-depth computer knowledge. Users are therefore        ##
## encouraged to load and test the software's suitability as regards their      ##
## requirements in conditions enabling the security of their systems and/or     ##
## data to be ensured and,  more generally, to use and operate it in the        ##
## same conditions as regards security.                                         ##
##                                                                              ##
## The fact that you are presently reading this means that you have had         ##
## knowledge of the CeCILL-C license and that you accept its terms.             ##
##                                                                              ##
##################################################################################
##################################################################################

##################################################################################
##################################################################################
##                                                                              ##
## Copyright Yoann Robin, 2018                                                  ##
##                                                                              ##
## yoann.robin.k@gmail.com                                                      ##
##                                                                              ##
## Ce logiciel est un programme informatique faisant partie de la librairie     ##
## Apyga. Cette librairie permet d'étudier les systèmes dynamique et de         ##
## corriger statistiquement des données en uni/multivarié en appliquant le      ##
## transport optimal à des histogrammes creux.                                  ##
##                                                                              ##
## Ce logiciel est régi par la licence CeCILL-C soumise au droit français et    ##
## respectant les principes de diffusion des logiciels libres. Vous pouvez      ##
## utiliser, modifier et/ou redistribuer ce programme sous les conditions       ##
## de la licence CeCILL-C telle que diffusée par le CEA, le CNRS et l'INRIA     ##
## sur le site "http://www.cecill.info".                                        ##
##                                                                              ##
## En contrepartie de l'accessibilité au code source et des droits de copie,    ##
## de modification et de redistribution accordés par cette licence, il n'est    ##
## offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,    ##
## seule une responsabilité restreinte pèse sur l'auteur du programme, le       ##
## titulaire des droits patrimoniaux et les concédants successifs.              ##
##                                                                              ##
## A cet égard  l'attention de l'utilisateur est attirée sur les risques        ##
## associés au chargement,  à l'utilisation,  à la modification et/ou au        ##
## développement et à la reproduction du logiciel par l'utilisateur étant       ##
## donné sa spécificité de logiciel libre, qui peut le rendre complexe à        ##
## manipuler et qui le réserve donc à des développeurs et des professionnels    ##
## avertis possédant  des  connaissances  informatiques approfondies.  Les      ##
## utilisateurs sont donc invités à charger  et  tester  l'adéquation  du       ##
## logiciel à leurs besoins dans des conditions permettant d'assurer la         ##
## sécurité de leurs systèmes et ou de leurs données et, plus généralement,     ##
## à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.           ##
##                                                                              ##
## Le fait que vous puissiez accéder à cet en-tête signifie que vous avez       ##
## pris connaissance de la licence CeCILL-C, et que vous en avez accepté les    ##
## termes.                                                                      ##
##                                                                              ##
##################################################################################
##################################################################################


###############
## Libraries ##
###############

import numpy as np
from Apyga.dynamic.__DynamicalSystem import DynamicalSystem
import scipy.integrate as sci

###########
## Class ##
###########

class DiffDynSyst(DynamicalSystem):
	"""
		Apyga.dynamic.continuous.DiffDynSyst
		====================================

		Description
		-----------
		Abstract base class to construct a continuous dynamical system.
		This class CAN NOT BE USED directly. It requires to be derived.
	"""

	def __init__( self , dim = 0 , size = 0 , bounds = None ):
		"""
			Initialisation of the continuous dynamical system

			Parameters
			----------
			dim    : int
			   Dimension of the phase space.
			size   : int
			   Numbers of initial condition simultaneously computed by the dynamical system
			bounds : np.array[ shape = (2,dim) ]
			   Bounds of a box in phase space where initial condition can be drawn.
					=> bounds[0,:] is the lower bound
					=> bounds[1,:] is the upper bound
			
			Attributes
			----------
			dim    : int
			   Dimension of the phase space.
			size   : int
			   Numbers of initial condition simultaneously computed by the dynamical system
			bounds : np.array[ shape = (2,dim) ]
			   Bounds of a box in phase space where initial condition can be drawn.
		"""
		DynamicalSystem.__init__( self , dim , size , bounds )
		self._edo_solver = "scipy"
		
	def _solver( self , X0 , time ):
		if self._edo_solver == "RK4":
			solution = np.zeros( (time.size,X0.size) )
			solution[0,:] = X0
			sTime = time.size - 1
			for i in range(sTime):
				h = time[i+1] - time[i]
				k1 = self._equation( solution[i,:] , time[i] )
				k2 = self._equation( solution[i,:] + h * k1 / 2. , time[i] + h / 2. )
				k3 = self._equation( solution[i,:] + h * k2 / 2. , time[i] + h / 2. )
				k4 = self._equation( solution[i,:] + h * k3 , time[i+1] )
				solution[i+1,:] = solution[i,:] + h * ( k1 + 2 * k2 + 2 * k3 + k4 ) / 6.
			return solution
		elif self._edo_solver == "Euler":
			solution = np.zeros( (time.size,X0.size) )
			solution[0,:] = X0
			sTime = time.size - 1
			for i in range(sTime):
				h = time[i+1] - time[i]
				solution[i+1,:] = solution[i,:] + h * self._equation( solution[i,:] , time[i] )
			return solution
		else:
			return sci.odeint( self , X0 , time )
		

