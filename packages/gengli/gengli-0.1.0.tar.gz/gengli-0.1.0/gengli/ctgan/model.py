"""
gengli.ctgan.model
==================

	Definition of the CTGAN architecture. It implements the generator `GenerativeNet` and the discriminator `DiscriminativeNet`, as well as two handy functions for weights initialization.
"""
import torch
import torch.nn as nn

cuda = True if torch.cuda.is_available() else False
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

############################
#   Create the Generator   #
############################


class GenerativeNet(torch.nn.Module):
	"""
	Class for the generator network for the CTGAN, implemented as a `torch.nn`. It is composed by a fully connected convolutional neural network.
	"""
	def __init__(self, num_channel_G):
		super(GenerativeNet, self).__init__()

		self.conv1 = nn.Sequential(
			nn.Upsample(size=120),
			(nn.Conv1d(in_channels=1, out_channels=num_channel_G*16,
					   kernel_size=5, stride=1, dilation=2,
					   padding=0, bias=False)),
			nn.BatchNorm1d(num_channel_G*16),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv2 = nn.Sequential(
			nn.Upsample(size=150),
			(nn.Conv1d(in_channels=num_channel_G*16,
					   out_channels=num_channel_G*8,
					   kernel_size=5, stride=1, dilation=4,
					   padding=0, bias=False)),
			nn.BatchNorm1d(num_channel_G*8),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv3 = nn.Sequential(
			nn.Upsample(size=170),
			(nn.Conv1d(in_channels=num_channel_G*8,
					   out_channels=num_channel_G*4,
					   kernel_size=5, stride=1, dilation=6,
					   padding=0, bias=False)),
			nn.BatchNorm1d(num_channel_G*4),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv4 = nn.Sequential(
			nn.Upsample(size=235),
			(nn.Conv1d(in_channels=num_channel_G*4,
					   out_channels=num_channel_G*2,
					   kernel_size=5, stride=1, dilation=8,
					   padding=0, bias=False)),
			nn.BatchNorm1d(num_channel_G*2),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv5 = nn.Sequential(
			nn.Upsample(size=470),
			(nn.Conv1d(in_channels=num_channel_G*2,
					   out_channels=num_channel_G,
					   kernel_size=5, stride=1, dilation=16,
					   padding=0, bias=False)),
			nn.BatchNorm1d(num_channel_G),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv6 = nn.Sequential(
			nn.Upsample(size=942),
			(nn.Conv1d(in_channels=num_channel_G,
					   out_channels=1, kernel_size=5,
					   stride=1, padding=0, bias=False)),
			nn.Tanh())

	def forward(self, x):

		x = self.conv1(x)
		x = self.conv2(x)
		x = self.conv3(x)
		x = self.conv4(x)
		x = self.conv5(x)
		x = self.conv6(x)

		return x

################################
#   Create the Discriminator   #
################################


class DiscriminativeNet(torch.nn.Module):
	"""
	Class for the discriminator network for the CTGAN, implemented as a `torch.nn`. It is composed by a fully connected convolutional neural network.
	```CHECK THIS```
	"""
	
	def __init__(self, dropout_rate, num_channel_D, batch_size):

		super(DiscriminativeNet, self).__init__()

		self.batch_size = batch_size

		self.conv1 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=1, out_channels=num_channel_D,
					   kernel_size=5, stride=2, padding=1, bias=False)),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv2 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D, out_channels=num_channel_D*2,
					   kernel_size=5, stride=2, padding=0, bias=False)),
			nn.Dropout(p=dropout_rate, inplace=True),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv3 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D*2,
					   out_channels=num_channel_D*4,
					   kernel_size=5, stride=2, padding=0, bias=False)),
			nn.Dropout(p=dropout_rate, inplace=True),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv4 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D*4,
					   out_channels=num_channel_D*8,
					   kernel_size=5, stride=2, padding=0, bias=False)),
			nn.Dropout(p=dropout_rate, inplace=True),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv5 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D*8,
					   out_channels=num_channel_D*16,
					   kernel_size=5, stride=2, padding=0, bias=False)),
			nn.Dropout(p=dropout_rate, inplace=True),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv6 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D*16,
					   out_channels=num_channel_D*32,
					   kernel_size=5, stride=2, padding=0, bias=False)),
			nn.Dropout(p=dropout_rate, inplace=True),
			nn.LeakyReLU(0.2, inplace=True))
		self.conv7 = nn.Sequential(
			nn.utils.spectral_norm
			(nn.Conv1d(in_channels=num_channel_D*32,
					   out_channels=1, kernel_size=11,
					   stride=2, padding=0, bias=False)),
			nn.Flatten())

	def forward(self, x):
		x = self.conv1(x)
		x = self.conv2(x)
		x = self.conv3(x)
		x = self.conv4(x)
		x = self.conv5(x)
		x_ = self.conv6(x)
		x = self.conv7(x_)
		x_ = x_.view(self.batch_size, -1)

		return x, x_

######################################################
#   Weights initialization called on netG and netD   #
######################################################


def init_weights(m):

	classname = m.__class__.__name__

	if classname.find('Conv') != -1:  # or classname.find('BatchNorm') != -1:
		m.weight.data.normal_(0.00, 0.02)

	elif classname.find('BatchNorm') != -1:
		m.weight.data.normal_(1.00, 0.02)


def init_weights2(m):

	classname = m.__class__.__name__

	if classname.find('Conv') != -1:  # or classname.find('BatchNorm') != -1:
		m.weight.data.normal_(0.00, 0.02)
	elif classname.find('LayerNorm') != -1:
		m.weight.data.normal_(1.00, 0.02)
