package Day14::Cave::ReadProperly;

use v5.36;
use Moo;

extends 'Day14::Cave';

sub BUILD ($self, $args)
{
	my $lowest = $self->lowest_wall;
	my @occupied_walls = $self->_occupied_walls->@*;

	# lazy hack to simulate infinity
	for (1 .. 500) {
		push @occupied_walls, [];
	}

	for my $ys (@occupied_walls) {
		$ys->[$lowest + 2] = !!1;
	}

	$self->_set_occupied_walls([map { $_ // [] } @occupied_walls]);
}

sub _fall_into_abyss ($self, $point)
{
	die "there's no abyss!";
}

sub into_abyss ($self, $position)
{
	return !!0;
}

1;

