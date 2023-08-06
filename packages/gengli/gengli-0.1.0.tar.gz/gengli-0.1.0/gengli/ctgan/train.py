"""
gengli.ctgan.train
==================
	
	Some functions to train the CTGAN model. The training procedure is implemented in `training_loop()`.
	The module provides also some helpers to load a glitch datasat
"""
import time
import numpy as np
import torch
from torch.autograd.variable import Variable
import torch.optim as optim
import os
from tqdm import tqdm

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
#####################
#   Training Loop   #
#####################

# NOTE: Loss function is defined as the Wasserstein loss
# and is not implemented directly in PyTorch. See training loop.
#Where is it implemented??

if torch.cuda.is_available():
	cuda = True
else:
	cuda = False

Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor


def training_loop(ifo, num_epochs, data_loader, ncycles_D, lambda_gp,
				  lambda_ct, M, batch_size, length_noise, device, netD,
				  netG, lr_D, lr_G, fixed_noise, safety_glitch,
				  save_dir):
	"""
	Training and validation loops for CTGAN.
	
	Parameters
	----------
	ifo: str
		Detector (it must be one of 'H1', 'L1', 'V1' or 'K1')
	num_epochs: int
		number of training epochs
	data_loader: torch.utils.data.DataLoader
		Torch data loader holding the training data
	ncycles_D: int
		Number of iterations of the Discriminator per iteration of the Generator
	lambda_gp: float
		Gradient Penalty (GP) term
	lambda_ct: float
		Consistency Term (CT) term
	M: float
		`#TODO: What is this??`
	batch_size: int 
		Number of batches for each iteration
	length_noise: int 
		Size of the noise vector
	device: torch.device
		Torch devide object. It is recommended to initialize it with a GPU
	netD: gengli.ctgan.DiscriminativeNet
		Discriminator network
	netG: gengli.ctgan.GenerativeNet
		Generator network
	lr_D: float 
		Learning rate for the discriminator
	lr_G: float
		Learning rate for the generator
	fixed_noise: torch.tensor
		Tensor holding fixed noise for sanity check
	safety_glitch: bool
		`#TODO: What is this??`
	save_dir: str
		Path to a directory where to store the weigths (subdir weights) and the loss function (subdir loss)
		If ``None``, the weigths and losses will not be saved

	"""
	# Taking care of the folders
	if isinstance(save_dir,str):
		if save_dir.endswith('/'): save_dir = save_dir[:-1]
		path_weights = '{}/weights/'.format(save_dir)
		path_loss = '{}/losses/'.format(save_dir)
		dir_list = [save_dir, path_weights, path_loss]

		if safety_glitch:
			path_fixed_glitch = '{}/fixed_glitch/'.format(save_dir)
			dir_list.append(path_fixed_glitch)

		for d in dir_list:		
			if not os.path.exists(d): os.mkdir(d)

	# Checking for the ifo
	allowed_ifos = ['H1', 'L1', 'V1', 'K1']
	assert (ifo in allowed_ifos), "Wrong ifo {} given: it must be in {}".format(ifo, allowed_ifos)

	# Set optimizer
	optimizerD = optim.RMSprop(netD.parameters(), lr=lr_D)
	optimizerG = optim.RMSprop(netG.parameters(), lr=lr_G)

	# Lists to keep track of progress
	G_losses = list()
	D_losses = list()
	D_real_losses = list()
	D_fake_losses = list()
	D_gp_losses = list()
	D_ct_losses = list()

	##
	# Training loop
	# Loops on epochs

	for epoch in tqdm(range(num_epochs), desc = 'CT-GAN training loop'):

		iters = 0
		start = time.time()

		# For each batch in the data
		for batch_real in data_loader:

			# Iterate ncycles_D times over the Discriminator
			for j in np.arange(ncycles_D):

				# (1) Update D network  #

				# Train with all-real batch
				# Zeroing the gradients
				netD.zero_grad()
				# Real batch generation
				data_real = batch_real.view(batch_size, 1, -1)
				data_real = data_real.to(device)
				data_real = data_real.float()  #casting to float #FIXME: is this ok also for GPU?
				# Forward pass real batch through D
				D_real, D_real_ = netD(data_real)
				D_real = D_real.view(-1)
				# Calculate loss on all-real batch
				errD_real = torch.mean(D_real)

				# Train with all-fake batch
				# Generate batch of latent vectors
				noise = torch.randn((batch_size, 1, length_noise),
									device=device)
				# Generate fake image batch with G
				data_fake = netG(noise)
				# Classify all fake batch with D
				D_fake, D_fake_ = netD(data_fake)
				D_fake = D_fake.view(-1)
				# Calculate D's loss on the all-fake batch
				errD_fake = torch.mean(D_fake)

				# Compute gradient penalty
				GP = compute_gradient_penalty(netD, data_real, data_fake)

				# Compute consistency term
				CT = compute_consistency_term(netD, data_real, M)

				# Add the gradients from the all-real and all-fake
				# batches + gradient penalty
				errD = -errD_real + errD_fake + lambda_gp*GP + lambda_ct*CT

				# Backward propagation of total loss and Update D
				errD.backward()
				optimizerD.step()

			#########################
			# (2) Update G network  #
			#########################
			# Zeroing the gradients
			netG.zero_grad()
			# Creating noise
			noise2 = torch.randn((batch_size, 1, length_noise), device=device)
			# Forward pass through G
			fake2 = netG(noise2)
			# Since we updated D, perform a forward pass of
			# all-fake batch through D
			output, output_ = netD(fake2)
			output = output.view(-1)
			# Calculate G's loss based on this output
			errG = -torch.mean(output)
			# Backward propagation of the loss and Update G
			errG.backward()
			optimizerG.step()

			# Save Losses for plotting later
			G_losses.append(errG.item())
			D_losses.append(errD.item())
			D_real_losses.append(-errD_real.item())
			D_fake_losses.append(errD_fake.item())
			D_gp_losses.append(lambda_gp*GP.item())
			D_ct_losses.append(lambda_ct*CT.item())

			iters += 1

		# Output training stats
		begin = epoch*len(data_loader)
		end = (epoch+1)*len(data_loader)
		error_D = np.mean(D_losses[begin:end])
		error_G = np.mean(G_losses[begin:end])
		error_D_real = np.mean(D_real_losses[begin:end])
		error_D_fake = np.mean(D_fake_losses[begin:end])
		error_D_gp = np.mean(D_gp_losses[begin:end])
		error_D_ct = np.mean(D_ct_losses[begin:end])
		end = time.time()

		if((epoch + 1) % 1 == 0):
			print('[%d/%d] Loss_D: %.3f | Loss_G: %.3f | Loss D real : %.3f | Loss D fake : %.3f | Loss D GP : %.3f | Loss D CT : %.3f | Time : %.3f' % (epoch+1, num_epochs, error_D, error_G, error_D_real, error_D_fake, error_D_gp, error_D_ct, np.mean(end-start)))

		# Check how the generator is doing by saving G's output on fixed_noise
		if((epoch + 1) % 10 == 0) and safety_glitch and isinstance(save_dir, str):
			with torch.no_grad():
				fake = netG(fixed_noise).detach().cpu()
				np.save('{}/output_epoch_{}.npy'.format(path_fixed_glitch, epoch+1),
						np.asarray(fake[0].detach().cpu().numpy()))

	if isinstance(save_dir, str):

			##
			# Saving weights

		# Save the state of the Generator and Discriminator
		torch.save(netG.state_dict(),
				'{}/blip_{}_CTGAN_state_G.pth'.format(path_weights, ifo))
		torch.save(netD.state_dict(),
				'{}/blip_{}_CTGAN_state_D.pth'.format(path_weights, ifo))

			##
			# Saving loss

		loss_G = np.asarray(G_losses)
		loss_D = np.asarray(D_losses)
		loss_D_real = np.asarray(D_real_losses)
		loss_D_fake = np.asarray(D_fake_losses)
		loss_D_gp = np.asarray(D_gp_losses)
		loss_D_ct = np.asarray(D_ct_losses)

		np.save(path_loss+'loss_G_new', loss_G)
		np.save(path_loss+'loss_D_new', loss_D)
		np.save(path_loss+'loss_D_real_new', loss_D_real)
		np.save(path_loss+'loss_D_fake_new', loss_D_fake)
		np.save(path_loss+'loss_D_gp_new', loss_D_gp)
		np.save(path_loss+'loss_D_ct_new', loss_D_ct)


def compute_gradient_penalty(D, real_samples, fake_samples):
	"""
		Function that computes gradient penalty.

	Parameters
	-----------
	D:
	real_samples:
	fake_samples:

	Returns
	-------
	gradient_penalty:

	# TODO
	"""
	# Random weight term for interpolation between real and fake samples
	alpha = Tensor(np.random.uniform(0, 1, (real_samples.size(0), 1, 1)))

	# Get random interpolation between real and fake samples
	interpolates = (alpha * real_samples + ((1 - alpha) * fake_samples))
	interpolates = interpolates.requires_grad_(True)

	d_interpolates, d_interpolates_ = D(interpolates)
	fake = Variable(Tensor(real_samples.shape[0], 1).fill_(1.0),
					requires_grad=False)

	# Get gradient w.r.t. interpolates
	gradients = torch.autograd.grad(outputs=d_interpolates,
									inputs=interpolates,
									grad_outputs=fake,
									create_graph=True,
									retain_graph=True,
									only_inputs=True)[0]

	gradients = gradients.view(gradients.size(0), -1)

	gradient_penalty = ((gradients.norm(2, dim=1) - 1)**2).mean()

	return gradient_penalty


def compute_consistency_term(D, real_data, M):
	"""

	Parameters
	----------
	D:
	real_data:
	M:

	Returns
	-------
	consistency_term.mean():

	# TODO
	"""
	d1, d_1 = D(real_data)
	d2, d_2 = D(real_data)

	first_term = (d1 - d2).norm(2, dim=1)
	second_term = (d_1 - d_2).norm(2, dim=1)

	consistency_term = first_term + 0.1 * second_term - M

	for i, item in enumerate(consistency_term):

		if (item < 0):
			consistency_term[i] = 0
	mean_consistency_term = consistency_term.mean()

	return mean_consistency_term
