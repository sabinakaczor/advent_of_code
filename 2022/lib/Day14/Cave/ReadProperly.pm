package Day14::Cave::ReadProperly;

use v5.36;
use Moo;
use Mooish::AttributeBuilder;
use Types::Common;

use constant ROCK => '#';

# this is a cave, duh

has field '_occupied_walls' => (
	isa => Types::Common::ArrayRef[Types::Common::ArrayRef[Types::Common::Bool]],
	writer => -hidden,
);

has field '_occupied_sand' => (
	isa => Types::Common::ArrayRef[Types::Common::ArrayRef[Types::Common::Bool]],
	default => sub { [] },
);

sub BUILD ($self, $args)
{
	my @lines = split /\n/, $args->{raw};

	my @occupied_walls;
	my $lowest = 0;

	for my $line (@lines) {
		my @positions = split /->/, $line;
		@positions = map {
			s/\s//g;
			[split /,/, $_]
		} @positions;

		my @last;
		for my $position (@positions) {
			$lowest = $position->[1]
				if $position->[1] > $lowest;

			$occupied_walls[$position->[0]][$position->[1]] = !!1;

			if (@last) {
				my $ch;
				my $step;

				if ($step = $last[0] <=> $position->[0]) {
					$ch = 0;
				}
				elsif ($step = $last[1] <=> $position->[1]) {
					$ch = 1;
				}
				else {
					die 'corrupted input';
				}

				my @range = $step < 0
					? $last[$ch] - $step .. $position->[$ch]
					: $position->[$ch] + $step .. $last[$ch]
				;

				for my $i (@range) {
					if ($ch == 0) {
						$occupied_walls[$i][$last[1]] = !!1;
					}
					else {
						$occupied_walls[$last[0]][$i] = !!1;
					}
				}
			}

			@last = $position->@*;
		}
	}

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

# returns whether sand move has stopped
sub be_poured ($self, $position)
{
	# try falling vertically
	return 0 if $self->find_next_vertically($position);

	# try falling to the side
	return 0 if $self->find_next_sides($position);

	# can't move - set this point occupied by sand
	my ($curr_x, $curr_y) = ($position->x, $position->y);
	$self->_occupied_sand->[$curr_x][$curr_y] = !!1;
	return 1;
}

sub at_rest ($self, $position)
{
	return $self->occupied($position->possible_falling_points, $position->possible_rolling_points);
}

sub into_abyss ($self, $position)
{
	return !!0;
}

# note: returns whether all @points are occupied
sub occupied ($self, @points)
{
	my $occupied_walls = $self->_occupied_walls;
	my $occupied_sand = $self->_occupied_sand;

	for my $point (@points) {
		my ($x, $y) = $point isa 'Day14::Point' ? ($point->x, $point->y) : $point->@*;

		if (!$occupied_walls->[$x][$y] && !$occupied_sand->[$x][$y]) {
			return !!0;
		}
	}

	return !!1;
}

sub find_next_vertically ($self, $point)
{
	my ($x, $y) = ($point->x, $point->y + 1);

	my $occupied_walls = $self->_occupied_walls->[$x];
	my $occupied_sand = $self->_occupied_sand->[$x];
	my $upto = $occupied_walls->@*;

	while ($y < $upto) {
		if ($occupied_walls->[$y] || $occupied_sand->[$y]) {
			my $moved = $point->y + 1 != $y;
			$point->fallen($y - 1) if $moved;
			return $moved;
		}

		$y += 1;
	}

	$self->_fall_into_abyss($point);
	return 1;
}

sub find_next_sides ($self, $position)
{
	my @next = $position->possible_rolling_points;

	for my $next_side (@next) {
		if (!$self->occupied($next_side)) {
			$position->set_x($next_side->[0]);
			$position->set_y($next_side->[1]);
			return 1;
		}
	}

	return 0;
}

1;

