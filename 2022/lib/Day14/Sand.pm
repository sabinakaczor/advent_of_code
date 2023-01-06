package Day14::Sand;

use v5.36;
use Moo;
use Mooish::AttributeBuilder;
use Types::Common;

use Day14::Position;

# this is sand - plural!

has param 'initial_pos' => (
	coerce => (Types::Common::InstanceOf['Day14::Position'])
		-> plus_coercions(Types::Common::ArrayRef, q{ Day14::Position->new(x => $_->[0], y => $_->[1]) }),
);

has param 'verbose' => (
	default => 1,
);

has field 'generation' => (
	isa => Types::Common::Int,
	writer => -hidden,
	default => 0,
);

sub inc_generation ($self)
{
	$self->_set_generation($self->generation + 1);
}

sub pour ($self, $cave)
{
	my $sand_lump = $self->initial_pos->clone;
	my $verbose = $self->verbose;

	while (-pouring) {
		while (-falling) {
			last if $cave->be_poured($sand_lump);
			return if $cave->into_abyss($sand_lump);

			say $sand_lump->as_string if $verbose;
		}

		$self->inc_generation;

		# looks like we're done - sand entrace is blocked
		return
			if $sand_lump->x == $self->initial_pos->x
			&& $sand_lump->y == $self->initial_pos->y;

		$sand_lump = $sand_lump->clone;
		while (-backtracing) {
			if ($sand_lump->backtrace) {
				if (!$cave->occupied($sand_lump)) {
					$sand_lump->fallen;
					last;
				}
			}
			else {
				$sand_lump = $self->initial_pos->clone;
				last;
			}
		}
	}
}

1;

